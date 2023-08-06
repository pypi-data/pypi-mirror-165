""" api init """
from wenxin_api.api.base_api import APIBaseObject
from wenxin_api.api.base_api import (CreatableAPIObject, 
                                     StopableAPIObject,
                                     DeletableAPIObject, 
                                     ListableAPIObject, 
                                     RetrievalableAPIObject
                                    )
from wenxin_api.api.task_api import Task
from wenxin_api.api.model_api import Model
from wenxin_api.api.dataset_api import Dataset
from wenxin_api.api.train_api import Train