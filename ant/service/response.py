#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json


class Status:
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class AntResponse(object):

    def __init__(self, status, instance=None, api=None, ops=None, msg=None, result=None, error=None, **kwargs):

        self.status = status
        self.instance = instance
        self.api = api
        self.ops = ops
        self.msg = msg
        self.result = result
        self.error = error

        for k, v in kwargs.items():
            if not hasattr(self, k):
                setattr(self, k, v)

    def add_attrs(self, **kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                setattr(self, k, v)

    def __str__(self):
        return json.dumps(self.__dict__)
