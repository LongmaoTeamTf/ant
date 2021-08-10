#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import Union
from pydantic import BaseModel


class API(object):

    def __init__(self, path: str, params=None):
        self._path = path
        self._params = params

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params


class CreateInstance(BaseModel):
    instance_name: str
    configs: dict


class DeleteInstance(BaseModel):
    instance_name: str


class GetInstanceInfo(BaseModel):
    instance_name: str


class BuildInstance(BaseModel):
    instance_name: str
    vectors: Union[str, list]
    ids: Union[str, list]
    mode: str


class InsertInstance(BaseModel):
    instance_name: str
    vectors: Union[str, list]
    ids: Union[str, list]
    mode: str


class UpdateInstance(BaseModel):
    instance_name: str
    vectors: Union[str, list]
    ids: Union[str, list]
    mode: str


class RemoveInstance(BaseModel):
    instance_name: str
    ids: Union[str, list]
    mode: str


class SearchInstance(BaseModel):
    instance_name: str
    vectors: list
    top_k: int
    nprobe: int = 10


class AntAPIs(object):
    LIST = API("/ant/list")
    INFO = API("/ant/info", GetInstanceInfo)
    CREATE = API("/ant/create", CreateInstance)
    DELETE = API("/ant/delete", DeleteInstance)
    BUILD = API("/ant/build", BuildInstance)
    INSERT = API("/ant/insert", InsertInstance)
    UPDATE = API("/ant/update", UpdateInstance)
    REMOVE = API("/ant/remove", RemoveInstance)
    SEARCH = API("/ant/search", SearchInstance)
    BGSAVE = API("/ant/bgsave")
