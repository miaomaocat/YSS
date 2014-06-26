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

    content_type_book = '0'
    content_type_music = '1'
    content_type_speech = '2'

    def __repr__(self):
        return "base model"

    def jsondict(self):
        return obj2dict(self)

    def typeName(self):
        if str(self.type) == '0':
            return u"书籍"
        elif str(self.type) == '1':
            return u"音乐"
        else:
            return u"讲座"
