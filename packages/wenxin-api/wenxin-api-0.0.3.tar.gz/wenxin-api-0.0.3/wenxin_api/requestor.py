# !/usr/bin/env python3
import json
import platform
import threading
import warnings
from json import JSONDecodeError
from typing import Dict, Iterator, Optional, Tuple, Union
from urllib.parse import urlencode, urlsplit, urlunsplit

import requests

import wenxin_api
from wenxin_api import error, log
from wenxin_api.base_object import BaseObject
from wenxin_api.error import (APIError, 
                              APIConnectionError, 
                              InvalidResponseValue, 
                              AuthenticationError,
                              ResponseDecodeError)
from wenxin_api.const import ERNIE_1P5B_MODEL
from wenxin_api.variable import ACCESS_TOKEN_URL, TIMEOUT_SECS, MAX_CONNECTION_RETRIES

# Has one attribute per thread, 'session'.
_thread_context = threading.local()
logger = log.get_logger()

from typing import Optional


class WenxinAPIResponse(BaseObject):
    def __init__(self, headers, request_type, **params):
        super(WenxinAPIResponse, self).__init__(**params)
        self._headers = headers
        self.type = request_type

    def __str__(self):
        return "WenxinAPIResponse {}:{}\n".format(
                        id(self),
                        json.dumps({"id": self.id, 
                                    "status": self.status,
                                    "type": self.type
                                   }, ensure_ascii=False)
        )

    def __repr__(self):
        return self.__str__()


def _requests_proxies_arg(proxy) -> Optional[Dict[str, str]]:
    if proxy is None:
        return None
    elif isinstance(proxy, str):
        return {"http": proxy, "https": proxy}
    elif isinstance(proxy, dict):
        return proxy.copy()
    else:
        raise ValueError(
            "'wenxin.proxy' must be url str or dict"
        )


def _make_session() -> requests.Session:
    s = requests.Session()
    proxies = _requests_proxies_arg(wenxin_api.proxy)
    if proxies:
        s.proxies = proxies
    s.mount(
        "https://",
        requests.adapters.HTTPAdapter(max_retries=MAX_CONNECTION_RETRIES),
    )
    return s


class HTTPRequestor:
    """ HTTP Requestor """ 
    def __init__(self, ak=None, sk=None, request_type=None):
        self.ak = ak
        self.sk = sk
        self.request_type = request_type
        self.access_token_post_url = ACCESS_TOKEN_URL
        
    def _get_access_token(self, ak=None, sk=None):
        if ak == None or sk == None:
            ak = wenxin_api.ak
            sk = wenxin_api.sk
        json_data = {
            "grant_type": "client_credentials",
            "client_id": ak,
            "client_secret": sk
        }
        method = "post" # hard code
        result = self._request(self.access_token_post_url, method, data=json_data)
        logger.debug("result of access token: {}".format(result.json()))
        return result.json()["data"]

    def request(self, url, method="post", headers=None, files=None, request_id=None, **params
    ) -> Union[WenxinAPIResponse, Iterator[WenxinAPIResponse]]:
        
        if isinstance(params, dict):
            data = params
            base_model = params.get("base_model", ERNIE_1P5B_MODEL)
            return_raw = params.pop("return_raw", False)
        else:
            data = {}
            base_model = ERNIE_1P5B_MODEL

        data["cmd"] = request_id
        data["base_model"] = base_model
        logger.debug("request id: {}, base_model: {}, request params: {}".format(
            request_id,
            base_model, 
            params))
        # try to use default access_token first
        # if auth failed, use dynamically generated access_token instead
        try:
            if wenxin_api.access_token != None:
                data["access_token"] =  wenxin_api.access_token
            else:
                access_token = self._get_access_token(self.ak, self.sk)
                data["access_token"] =  access_token
                wenxin_api.access_token = access_token
            result = self._request(url, method=method, headers=headers, data=data, files=files)
            logger.debug("request body:{}".format(json.dumps({
                    "url": url,
                    "method": method,
                    "headers": headers,
                    "data": data,
                    "files": len(files) if files else None},
                    ensure_ascii=False,
                    indent=2))
            )
            logger.debug("response: code {}: {}".format(
                result.status_code,
                json.dumps(result.json(), 
                           ensure_ascii=False, 
                           indent=2)
            ))
        except AuthenticationError as e:
            access_token = self._get_access_token(self.ak, self.sk)
            data["access_token"] =  access_token
            wenxin_api.access_token = access_token
            result = self._request(url, method=method, headers=headers, data=data, files=files)

        if return_raw:
            return result
        else:
            resp = self._resolve_response(result.content, result.status_code, result.headers)
            return resp

    def _request(self, url, method="post", headers=None, data=None, files=None) -> requests.Response:
        if headers is None:
            headers = {"Content-Type": "application/json"}
        if not hasattr(_thread_context, "session"):
            _thread_context.session = _make_session()
        try:
            if isinstance(headers, dict) and \
               "Content-Type" in headers and \
               headers["Content-Type"] == "application/json":
                result = _thread_context.session.request(
                    method,
                    url,
                    headers=headers,
                    json=data,
                    timeout=TIMEOUT_SECS,
                )
            else:
                result = _thread_context.session.request(
                method,
                url,
                headers=headers,
                data=data,
                files=files,
                timeout=TIMEOUT_SECS,
            )
        except requests.exceptions.RequestException as e:
            raise error.APIConnectionError("error communicating with wenxin api") from e
        return result

    def _resolve_response(self, rbody, rcode, rheaders) -> WenxinAPIResponse:

        try:
            if hasattr(rbody, "decode"):
                rbody = rbody.decode("utf-8")
            data = json.loads(rbody)
        except (JSONDecodeError, UnicodeDecodeError):
            raise error.APIError(
                f"HTTP code {rcode} from API ({rbody})", rbody, rcode, headers=rheaders
            )

        if rcode != 200 or data["code"] != 0:
            raise self._request_error_handling(rbody, rcode, data, rheaders)

        if len(data["data"]) == 0:
            # some method ex. delete returns null data
            resp = WenxinAPIResponse(rheaders, self.request_type)
        elif self.request_type not in data["data"]:
            # some method  ex. create only returns ${type}_id
            resp = WenxinAPIResponse(rheaders, self.request_type, **data["data"])
        elif isinstance(data["data"][self.request_type], dict):
            resp = WenxinAPIResponse(rheaders, self.request_type, **data["data"][self.request_type])
        elif isinstance(data["data"][self.request_type], list):
            resp = [
                WenxinAPIResponse(rheaders, self.request_type, **one_data) \
                    for one_data in data["data"][self.request_type]
            ]
        else:
            raise ResponseDecodeError(json.dumps(data, ensure_ascii=False, indent=2))

        return resp

    def _request_error_handling(self, rbody, rcode, resp, rheaders):

        logger.error("wenxin api error {}: {}".format(rcode, rbody))
        error_msg = resp.get("error", "")

        if rcode == 200:
            msg = "API error code {}: {}".format(resp["code"], resp["msg"])
            return error.APIError(msg)

        elif rcode == 500:
            body_code = resp.get("code", None)
            if body_code == 18:
                return error.RateLimitError()
            elif body_code == 100 or body_code == 110:
                return error.AuthenticationError()
            elif body_code == 111:
                return error.AccessTokenExpiredError()
            else:
                msg = "API error code {}: {}".format(resp["code"], resp["msg"])
                return error.APIError(msg)

        elif rcode == 503:
            raise error.ServiceUnavailableError(
                "The server is overloaded or not ready yet.",
                rbody,
                rcode,
                headers=rheaders,
            )

        elif rcode in [400, 404, 415]:
            return error.InvalidRequestError(
                error_msg,
                rbody,
                rcode,
                resp,
                rheaders,
            )

        else:
            return error.APIError(error_msg, rbody, rcode, resp, rheaders)