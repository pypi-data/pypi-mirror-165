# !/usr/bin/env python3
""" task api """
import time
import json
from wenxin_api.api.base_api import CreatableAPIObject, ListableAPIObject, StopableAPIObject, RetrievalableAPIObject
from wenxin_api.api.model_api import Model
from wenxin_api.base_object import BaseObject
from wenxin_api.error import APIError, IllegalRequestArgumentError, MissingRequestArgumentError
from wenxin_api.const import INFERENCE_TASK
from wenxin_api.const import (CMD_DO_DEPLOY, 
                              CMD_DO_INFERENCE, 
                              CMD_QUERY_MODEL, 
                              CMD_QUERY_TASK,
                              CMD_STOP_TASK,)
from wenxin_api.const import (MODEL_STATE_ERROR, 
                              MODEL_STATE_SUCCESS, 
                              MODEL_STATE_ON_SERVICE,)
from wenxin_api.const import (TASK_STATE_INFER_IN_QUEUE,
                              TASK_STATE_INFER_RUNNING,
                              TASK_STATE_INFER_END,)
from wenxin_api.const import (TASK_STATE_DEPLOY_SUBMIT, 
                              TASK_STATE_DEPLOY_IN_QUEUE, 
                              TASK_STATE_DEPLOY_RUNNING,
                              TASK_STATE_DEPLOY_SUCCESS,
                              TASK_STATE_DEPLOY_FAILED,)
from wenxin_api.const import ERNIE_100B_MODEL
from wenxin_api.variable import REQUEST_SLEEP_TIME
from wenxin_api import log
logger = log.get_logger()

class Task(CreatableAPIObject, ListableAPIObject, StopableAPIObject, RetrievalableAPIObject):
    """ task class """
    OBJECT_NAME = "tasks"

    @staticmethod
    def _resolve_result(resp):
        rst = {}
        rst["result"] = resp["output"]["result"]
        return rst

    @classmethod
    def create(cls, text=None, model=None, **params):
        if text is None:
            raise IllegalRequestArgumentError("text shouldn't be none")

        if model is None:
            # provide by default
            model = Model.retrieve(model_id=ERNIE_100B_MODEL)
        else:
            model.update()
        # deploy
        if model.status != MODEL_STATE_ON_SERVICE:
            request_id = CMD_DO_DEPLOY
            params["type"] = "task"
            deploy_task = super().create(model_id=model.id, request_id=request_id, **params)

            not_ready = True
            while not_ready:
                deploy_task.update()
                not_ready = deploy_task.status != TASK_STATE_DEPLOY_SUCCESS
                if deploy_task.status == TASK_STATE_DEPLOY_FAILED:
                    raise APIError("deploy task:{} failed".format(deploy_task.id))
                logger.info("model is preparing now!, task_id:{}, status:{}".format(
                    deploy_task.id, 
                    deploy_task.status)
                )
                time.sleep(REQUEST_SLEEP_TIME)
        
        # inference
        logger.info("model {}: starts writing".format(model.id))
        request_id = CMD_DO_INFERENCE
        # todo:add base_model and is_prompt
        # api_type 10 for inference
        resp = cls.default_request(text=text, 
                                   model_id=model.id, 
                                   api_type=10, 
                                   request_id=request_id, 
                                   **params)
        return cls._resolve_result(resp)

    @classmethod
    def list(cls, *args, **params):
        """ list """
        request_id = CMD_QUERY_TASK
        params["type"] = "task"
        resps = super().list(request_id=request_id, **params)
        filtered_resps = [resp for resp in resps \
                            if resp.status >= 300 and \
                               resp.status < 400]
        return filtered_resps

    @classmethod
    def retrieve(cls, *args, **params):
        """ retrieve """
        request_id = CMD_QUERY_TASK
        params["type"] = "task"
        if "task_id" not in params:
            raise MissingRequestArgumentError("task_id is not provided")
        return super().retrieve(request_id=request_id, **params)

    def stop(self, *args, **params) -> BaseObject:
        request_id = CMD_STOP_TASK
        params["type"] = "task"
        params["task_type"] = INFERENCE_TASK
        params["task_id"] = self.id
        if self.id is None:
            raise IllegalRequestArgumentError("illegal task_id")
        super().stop(request_id=request_id, **params)
        self.update()

    def update(self, *args, **params):
        """ update """
        request_id = CMD_QUERY_TASK
        params["type"] = "task"
        task = super().retrieve(task_id=self.id, request_id=request_id, **params)
        self.refresh_from(task)

    def __str__(self):
        return "Task {}:{}".format(
                        id(self),
                        json.dumps({"id": self.id, 
                                    "status": self.status,
                                    "type": self.type
                                   }, ensure_ascii=False)
        )

    def __repr__(self):
        return self.__str__()


