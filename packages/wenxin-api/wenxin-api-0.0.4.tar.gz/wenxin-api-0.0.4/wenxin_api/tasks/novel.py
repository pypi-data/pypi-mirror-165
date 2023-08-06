""" paragraph task """
from wenxin_api.api import Task
from wenxin_api.error import IllegalRequestArgumentError
from wenxin_api import log
logger = log.get_logger()

class Novel(Task):
    """ novel task """
    @staticmethod
    def _resolve_result(resp):
        rst = {}
        rst["result"] = resp["result"]
        return rst

    @classmethod
    def create(cls, text=None, model=None, **params):
        """ create """
        if text is None:
            raise IllegalRequestArgumentError("text shouldn't be none")
        model_id = 1 if model is None else model.id
        # params["seq_len"] = params.get("seq_len", 512)
        # params["topp"] = params.get("topp", 0.9)
        # params["penalty_score"] = params.get("penalty_score", 1.2)
        # params["min_dec_len"] = params.get("min_dec_len", 2)
        # params["min_dec_penalty_text"] = params.get("min_dec_penalty_text", "。？：！[<S>]")
        # params["is_unidirectional"] = params.get("is_unidirectional", 1)
        # params["task_prompt"] = params.get("task_prompt", "novel")
        # params["logits_bias"] = params.get("logits_bias", -5)
        # params["mask_type"] = params.get("mask_type", "paragraph")
        # params["text"] = "上文：{} 下文：".format(params["text"])
        params["api_type"] = params.get("api_type", 6)
        logger.info("model {}: starts writing".format(model_id))
        resp = cls.default_request(text=text, **params)
        return cls._resolve_result(resp)