#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from logging import Formatter


class LoggerHandler(metaclass=ABCMeta):

    @abstractmethod
    def build(self, formatter: Formatter):
        NotImplementedError()
