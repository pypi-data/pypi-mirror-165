""" dataset api """
import json
import os
import time

import wenxin_api
from wenxin_api import requestor, error, log
from wenxin_api.api import CreatableAPIObject, ListableAPIObject, DeletableAPIObject, RetrievalableAPIObject
from wenxin_api.error import MissingRequestArgumentError, FileError
from json import JSONDecodeError
from wenxin_api.const import CMD_UPLOAD_DATA, CMD_QUERY_DATA, CMD_DELETE_DATA, FILE_LINE_UPPER_BOUND
from wenxin_api.variable import REQUEST_SLEEP_TIME
logger = log.get_logger()


class Dataset(CreatableAPIObject, ListableAPIObject, DeletableAPIObject, RetrievalableAPIObject):
    """ dataset api """

    @staticmethod
    def _check_file_line(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    json_line = json.loads(line)
                    src = json_line.get("src", None)
                    tgt = json_line.get("tgt", None)
                    if src is None or tgt is None:
                        raise FileError("missing src or tgt column")
                    if len(src) > FILE_LINE_UPPER_BOUND or len(tgt) > FILE_LINE_UPPER_BOUND:
                        raise FileError("the file line exceeded the maximum word limit!")
                except JSONDecodeError as e:
                    raise FileError("input file must be in json format")


    @classmethod
    def create(cls, local_file_path, **params):
        """ create """
        cls._check_file_line(local_file_path)
        timeout = params.pop("timeout", None)
        if "data_name" not in params:
            params["data_name"] = "test"
        params["type"] = "data"

        files = {"url": ("test", open(local_file_path, 'rb'))}
        request_id = CMD_UPLOAD_DATA
        headers = {}
        resp = cls.default_request(headers=headers,
                                   request_id=request_id, 
                                   files=files,
                                   **params)
        dataset = cls.retrieve(data_id=resp.id)
        return dataset

    @classmethod
    def retrieve(cls, *args, **params):
        """ retrieve """
        request_id = CMD_QUERY_DATA
        params["type"] = "data"
        if "data_id" not in params:
            raise MissingRequestArgumentError("data_id is not provided")
        resp = super().retrieve(request_id=request_id, **params)
        return resp

    @classmethod
    def list(cls, *args, **params):
        """ list """
        request_id = CMD_QUERY_DATA
        params["type"] = "data"
        resp = super().list(request_id=request_id, **params)
        return resp

    @classmethod
    def delete(cls, *args, **params):
        """ delete """
        request_id = CMD_DELETE_DATA
        params["type"] = "data"
        if "data_id" not in params:
            raise MissingRequestArgumentError("data_id is not provided")
        return super().delete(request_id=request_id, **params)

    def __str__(self):
        return "Dataset {}:{}".format(
                        id(self),
                        json.dumps({"id": self.id, 
                                    "name": self.get("data_name", ""),
                                    "url": self.get("url", ""),
                                    "md5": self.get("md5", ""),
                                    "type": self.type
                                   }, ensure_ascii=False)
        )

    def __repr__(self):
        return self.__str__()
