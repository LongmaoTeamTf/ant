#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import yaml
import shutil

from ant.core.top_k_search import TopKSearch


class MultiInstances(object):

    __instances = {}

    __conf__ = ['data_dir', 'version', 'configs']

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance"):
            cls.__instance = super(MultiInstances, cls).__new__(cls)

        return cls.__instance

    def __init__(self, data_dir):
        super().__init__()

        self._data_dir = data_dir
        self._members_dir = os.path.join(self._data_dir, "members")

        if not os.path.exists(self._data_dir):
            raise FileNotFoundError(self._data_dir)

        if os.path.exists(self._members_dir):
            self.initialization()
        else:
            os.mkdir(self._members_dir)

    def initialization(self):

        for member_name in os.listdir(self._members_dir):
            if os.path.isfile(member_name):
                continue
            member_dir = os.path.join(self._members_dir, member_name)
            config_file = os.path.join(member_dir, "conf.yml")
            if not os.path.exists(config_file):
                print("`{}` instance's `conf.yml` missing. Skipped.".format(member_name))
                continue
            conf_obj = self.load_instance_conf(config_file)

            if self.check_config_file(conf_obj) is False:
                continue

            instance = TopKSearch(conf_obj["data_dir"], conf_obj["version"], **conf_obj["configs"])
            instance.rebuild()

            self.__instances[member_name] = {}
            self.__instances[member_name]["instance"] = instance
            self.__instances[member_name]["data_dir"] = conf_obj["data_dir"]
            self.__instances[member_name]["version"] = conf_obj["version"]
            self.__instances[member_name]["configs"] = conf_obj["configs"]

    def get_instance(self, instance_name):
        if self.__instances.get(instance_name) is not None:
            return self.__instances[instance_name]["instance"]

    def get_instance_conf(self, instance_name):
        if self.__instances.get(instance_name) is not None:
            _instance = self.__instances[instance_name]
            _instance.pop("instance")
            return _instance

    def list_instances(self):
        return [ins for ins in self.__instances]

    def create_instance(self, instance_name, configs: dict):
        if self.__instances.get(instance_name) is not None:
            raise ValueError("Instance `{}` is exist.".format(instance_name))

        instance_dir = os.path.join(self._members_dir, instance_name)
        if not os.path.exists(instance_dir):
            os.mkdir(instance_dir)

        version = TopKSearch.get_strtime(fmt="%Y%m%d%H%M%S%f")

        self.__instances[instance_name] = {}
        self.__instances[instance_name]["instance"] = TopKSearch(instance_dir, version, **configs)
        self.__instances[instance_name]["data_dir"] = instance_dir
        self.__instances[instance_name]["version"] = version
        self.__instances[instance_name]["configs"] = configs

        self.save_instance_conf(instance_name)

    def delete_instance(self, instance_name):
        shutil.rmtree(self.__instances[instance_name]["data_dir"])
        self.__instances.pop(instance_name)

    def save_instance_conf(self, instance_name):
        _skip_conf = ["instance"]
        config_obj = self.__instances.get(instance_name)
        if config_obj is None:
            raise ValueError("Instance `{}` is not exist.".format(instance_name))
        _fn = os.path.join(config_obj["data_dir"], "conf.yml")
        conf = {}
        for k, v in config_obj.items():
            if k in _skip_conf:
                continue
            conf[k] = v
        with open(_fn, "w") as f:
            yaml.dump(conf, f)

    def update_instance_version(self, instance_name, version):
        self.__instances[instance_name]["version"] = version

    @staticmethod
    def load_instance_conf(config_file):
        with open(config_file, "r") as f:
            conf = yaml.load(f.read(), Loader=yaml.FullLoader)
        return conf

    def check_config_file(self, conf_obj):

        def is_pass(key):
            value = conf_obj.get(key)
            if value is None:
                print("`{}` is missing in the `conf.yml`. Skipped".format(key))
                return False
            return True

        for k in self.__conf__:
            if is_pass(k) is False:
                return False
        return True
