#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
from logging import Formatter
from ant.logger.handlers import FileHandler
from ant.logger.handlers import ElasticsearchHandler


class AntLogger(object):

    def __init__(self,
                 name: str = "ant",
                 fmt: str = None,
                 level: str = "DEBUG",
                 log_enable: bool = True,
                 log_to_console: bool = True,
                 log_to_file: bool = False,
                 log_to_elasticsearch: bool = False,
                 tz="Asia/Shanghai"):

        self._name = name
        self._fmt = fmt
        self._level = level
        self._log_enable = log_enable
        self._log_to_console = log_to_console
        self._log_to_file = log_to_file
        self._log_to_elasticsearch = log_to_elasticsearch
        self._tz = tz

        os.environ['TZ'] = self._tz
        time.tzset()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance"):
            cls.__instance = super(AntLogger, cls).__new__(cls)

        return cls.__instance

    def __call__(self, configs: dict, *args, **kwargs):
        logger = logging.getLogger(self._name)
        logger.setLevel(self._level)
        formatter = Formatter(self._fmt)

        if self._log_enable and self._log_to_console:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(level=self._level)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        if self._log_enable and self._log_to_file:
            conf_obj = configs.get("file")
            if conf_obj is None:
                raise ValueError("When `log_to_file` is True, the configs of `file` is missing.")

            if conf_obj.get("logger_dir") is None:
                raise ValueError("`logger_dir` is missing.")

            file_handler = FileHandler(**conf_obj).build(formatter)
            logger.addHandler(file_handler)

        if self._log_enable and self._log_to_elasticsearch:
            conf_obj = configs.get("elasticsearch")
            if conf_obj is None:
                raise ValueError("When `log_to_elasticsearch` is True, "
                                 "the configs of `elasticsearch` is missing.")

            for param_key in ("host", "port", "user", "password", "index_name"):
                if conf_obj.get(param_key) is None:
                    raise ValueError("`{}` is missing.".format(param_key))

            es_handler = ElasticsearchHandler(**conf_obj).build(formatter)
            logger.addHandler(es_handler)

        return logger
