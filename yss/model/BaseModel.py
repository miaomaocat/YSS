# -*- coding: utf-8 -*-

from yss.controller.Common import *

def obj2dict(obj):
    """
        summary:
        将object转换成dict类型
    """
    _dict = {}
    for key, value in vars(obj).items():
        _dict[key] = value

    return _dict

class BaseModel(object):

    def __repr__(self):
        return "base model"

    def jsondict(self):
        return obj2dict(self)
