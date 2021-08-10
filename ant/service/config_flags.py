#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import yaml


class Configs(object):

    def __init__(self, config_obj: dict, name: str = None):
        self._config_obj = config_obj
        self._name = name

    @property
    def dict(self):
        return self._config_obj

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __call__(self, *args, **kwargs):
        for k, v in self._config_obj.items():
            if not hasattr(self, k):
                if isinstance(v, dict):
                    setattr(self, k, Configs(v, name=k)())
                    continue
                setattr(self, k, v)
        return self


class ConfigFlags(object):

    CONFIGS_DIR = "ant/configs"
    __slots__ = ("logger", "service")

    def __init__(self):

        config_files = os.listdir(self.CONFIGS_DIR)

        if not config_files:
            expected_files = [file + ".yml" for file in self.__slots__]
            raise ValueError("{} is empty. {} are missing.".format(self.CONFIGS_DIR, expected_files))

        self.load()

    def load(self):
        for config_files in os.listdir(self.CONFIGS_DIR):
            config_name = config_files.split(".")[0]
            with open(os.path.join(self.CONFIGS_DIR, config_files), "r") as f:
                config_obj = yaml.load(f.read(), Loader=yaml.FullLoader)
            config = Configs(config_obj, name=config_name)()
            if not hasattr(self, config_name):
                setattr(self, config_name, config)
