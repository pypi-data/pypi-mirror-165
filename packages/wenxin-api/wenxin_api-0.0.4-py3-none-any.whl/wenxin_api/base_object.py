# !/usr/bin/env python3
""" base object """

class BaseObject(dict):
    """ base object """
    def __init__(self, **params):
        super(BaseObject, self).__init__()
        for k, v in params.items():
            self.__setattr__(k, v)

    def __setattr__(self, k, v):
        if k[0] == "_" or k in self.__dict__:
            super(BaseObject, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == "_":
            raise AttributeError(k)
        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    @property
    def id(self):
        return self.get(f"{self.type}_id", "")

    @property
    def status(self):
        return self.get(f"{self.type}_state", None)

    def refresh_from(self, new_obj):
        for k, v in new_obj.items():
            self.__setattr__(k, v)

    @classmethod
    def construct_from(cls, values):
        instance = cls(**values)
        return instance