# -*- coding: utf-8 -*-
from flask import g, request
import sqlite3
class BaseModel(object):

    def __repr__(self):
        return "base model"
