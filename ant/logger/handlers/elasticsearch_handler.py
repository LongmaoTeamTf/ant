#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cmreslogging.handlers import CMRESHandler
from ant.logger.handler import LoggerHandler


class ElasticsearchHandler(LoggerHandler):

    def __init__(self, host, port, user, password, index_name, env: str = "default", level: str = "DEBUG"):
        super(ElasticsearchHandler, self).__init__()

        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._index_name = index_name
        self._env = env
        self._level = level

    def build(self, formatter):
        es_handler = CMRESHandler(hosts=[{"host": self._host, "port": self._port}],
                                  auth_type=CMRESHandler.AuthType.BASIC_AUTH,
                                  auth_details=(self._user, self._password),
                                  es_index_name=self._index_name,
                                  index_name_frequency=CMRESHandler.IndexNameFrequency.MONTHLY,
                                  es_additional_fields={"environment": self._env})
        es_handler.setLevel(level=self._level)
        es_handler.setFormatter(formatter)
        return es_handler
