""" cloze """
from wenxin_api.api import Task
from wenxin_api.error import IllegalRequestArgumentError
from wenxin_api import log
logger = log.get_logger()
class Cloze(Task):
    """ cloze task """
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
        # params["topp"] = params.get("topp", 0.3)
        # params["penalty_score"] = params.get("penalty_score", 1.2)
        # params["is_unidirectional"] = params.get("is_unidirectional", 0)
        # params["min_dec_len"] = params.get("min_dec_len", 1)
        # params["task_prompt"] = params.get("task_prompt", "cloze")
        # params["text"] = params["text"].replace("_", "[MASK]")
        params["api_type"] = params.get("api_type", 7)
        logger.info("model {}: starts writing".format(model_id))
        resp = cls.default_request(text=text, **params)
        return cls._resolve_result(resp)
