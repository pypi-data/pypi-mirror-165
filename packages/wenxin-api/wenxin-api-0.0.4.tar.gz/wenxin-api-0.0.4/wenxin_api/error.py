""" wenxin exceptions"""
import wenxin_api


class WenxinError(Exception):
    """ base wenxin error """
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super(WenxinError, self).__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:
                http_body = (
                    "could not decode body as utf-8."
                )

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.request_id = self.headers.get("request-id", None)

    def __str__(self):
        msg = self._message or "<empty message>"
        if self.request_id is not None:
            return "Request {0}: {1}".format(self.request_id, msg)
        else:
            return msg

    @property
    def user_message(self):
        """ user message """
        return self._message

    def __repr__(self):
        return "%s(message=%r, http_status=%r, request_id=%r)" % (
            self.__class__.__name__,
            self._message,
            self.http_status,
            self.request_id,
        )


class APIError(WenxinError):
    """ error returns by api server """
    pass


class TimeOutError(WenxinError):
    """ timeout error """
    pass


class NotReady(WenxinError):
    """ not ready error """
    pass


class APIConnectionError(WenxinError):
    """ api connection error """
    def __init__(
        self,
        message,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        should_retry=False,
    ):
        super(APIConnectionError, self).__init__(
            message, http_body, http_status, json_body, headers, code
        )
        self.should_retry = should_retry


class InvalidRequestError(WenxinError):
    """ invalid request error """
    def __init__(
        self,
        message,
        param,
        code=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
    ):
        super(InvalidRequestError, self).__init__(
            message, http_body, http_status, json_body, headers, code
        )
        self.param = param

    def __repr__(self):
        return "%s(message=%r, param=%r, code=%r, http_status=%r, " "request_id=%r)" % (
            self.__class__.__name__,
            self._message,
            self.param,
            self.code,
            self.http_status,
            self.request_id,
        )

    def __reduce__(self):
        return type(self), (
            self._message,
            self.param,
            self.code,
            self.http_body,
            self.http_status,
            self.json_body,
            self.headers,
        )

class FileError(WenxinError):
    """ file error """
    pass

class IllegalRequestArgumentError(WenxinError):
    """ illeagal request argument error """
    pass


class MissingRequestArgumentError(WenxinError):
    """ missing request argument error """
    pass


class InvalidResponseValue(WenxinError):
    """ invalid response value error """
    pass


class InternalServerError(WenxinError):
    """ internal server error """
    pass


class AuthenticationError(WenxinError):
    """ authentication error """
    pass

class AccessTokenExpiredError(WenxinError):
    """ access_token expired error """
    pass

class RateLimitError(WenxinError):
    """ qps limit error """
    pass

class ResponseDecodeError(WenxinError):
    """ response decode error """
    pass


class ServiceUnavailableError(WenxinError):
    """ service unavailable error """
    pass




