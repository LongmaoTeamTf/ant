#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from ant.logger.handler import LoggerHandler


class FileHandler(LoggerHandler):

    def __init__(self, logger_dir, logger_filename: str = "ant", when: str = "MIDNIGHT", backup_count: int = 10, level: str = "DEBUG"):
        super(FileHandler, self).__init__()

        self._logger_dir = logger_dir
        self._logger_filename = logger_filename
        self._when = when
        self._backup_count = backup_count
        self._level = level

        if not os.path.exists(self._logger_dir):
            os.makedirs(self._logger_dir)

    def build(self, formatter: Formatter):
        filename = os.path.join(self._logger_dir, self._logger_filename)

        file_handler = TimedRotatingFileHandler(filename,
                                                when=self._when,
                                                backupCount=self._backup_count)

        file_handler.setLevel(level=self._level)
        file_handler.setFormatter(formatter)
        return file_handler
