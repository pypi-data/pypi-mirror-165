""" text generation task """
from wenxin_api.api import Task
from wenxin_api.error import IllegalRequestArgumentError
from wenxin_api import log
logger = log.get_logger()


class TextGeneration(Task):
    """ text generation task """
    @staticmethod
    def _resolve_result(resp):
        rst = {}
        rst["result"] = resp["result"]
        return rst

    @classmethod
    def create(cls, text=None, model=None, **params):
        if text is None:
            raise IllegalRequestArgumentError("text shouldn't be none")
        model_id = 1 if model is None else model.id
        # inference
        # params["seq_len"] = params.get("seq_len", 512)
        # params["topp"] = params.get("topp", 0.9)
        # params["penalty_score"] = params.get("penalty_score", 1.2)
        # params["min_dec_len"] = params.get("min_dec_len", 4)
        # params["is_unidirectional"] = params.get("is_unidirectional", 1)
        # params["task_prompt"] = params.get("task_prompt", "PARAGRAPH")
        # params["penalty_text"] = params.get("penalty_text", "[{[gEND]")
        # params["min_dec_penalty_text"] = params.get("min_dec_penalty_text", "。？：！[<S>]")
        # params["logits_bias"] = params.get("logits_bias", -10)
        # params["mask_type"] = params.get("mask_type", "paragraph")
        params["api_type"] = params.get("api_type", 8)
        logger.info("model {}: starts writing".format(model_id))
        resp = cls.default_request(text=text, **params)
        return cls._resolve_result(resp)