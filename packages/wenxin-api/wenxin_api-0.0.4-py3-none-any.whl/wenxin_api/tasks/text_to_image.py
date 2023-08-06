""" text generation task """
import time
import warnings
import json
from wenxin_api import requestor, error, log
from wenxin_api.api import Task
from wenxin_api.api import ListableAPIObject
from wenxin_api.variable import REQUEST_SLEEP_TIME, VILG_CREATE_URL, VILG_RETRIEVE_URL
from wenxin_api.error import APIError
logger = log.get_logger()

class TextToImage(Task):
    """ text generation task """
    OBJECT_NAME = "text_to_image"
    @classmethod
    def create(cls, *args, **params):
        """ create """
        # hard code
        create_url = VILG_CREATE_URL
        retrieve_url = VILG_RETRIEVE_URL
        start = time.time()
        timeout = params.pop("timeout", None)
        text = params.pop("text", "")
        style = params.pop("style", "")
        http_requestor = requestor.HTTPRequestor()
        resp = http_requestor.request(create_url, text=text, style=style, return_raw=True)
        try:
            task_id = resp.json()["data"]["taskId"]
        except Exception as e:
            raise APIError(json.dumps(resp.json(), 
                           ensure_ascii=False,
                           indent=2))
        not_ready = True
        while not_ready:
            resp = http_requestor.request(retrieve_url, taskId=task_id, return_raw=True)
            not_ready = resp.json()["data"]["status"] == 0
            if not not_ready:
                return cls._resolve_result(resp.json())
            rst = resp.json()
            logger.info("model is painting now!, taskId: {}, waiting: {}".format(
                rst["data"]["taskId"],
                rst["data"]["waiting"]))
            time.sleep(REQUEST_SLEEP_TIME)

    @staticmethod
    def _resolve_result(resp):
        if resp["code"] == 0:
            ret_dict = {"imgUrls": []}
            for d in resp["data"]["imgUrls"]:
                ret_dict["imgUrls"].append(d["image"])
            return ret_dict
        else:
            return resp
