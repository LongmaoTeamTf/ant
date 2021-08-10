#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import uuid
import datetime as dt
from functools import wraps

import numpy as np


def _warp_dtype_check(*dtypes):
    def checker(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            match_args = []
            class_obj, true_args = args[0], args[1:]
            assert len(true_args) == len(dtypes), "Error: len(args) != len(dtypes)"
            for arg, dtype in zip(true_args, dtypes):
                if not isinstance(arg, np.ndarray):
                    arg = np.asarray(arg)
                if arg.dtype != dtype:
                    arg = arg.astype(dtype)
                match_args.append(arg)
            return func(class_obj, *match_args, **kwargs)

        return wrapper

    return checker


def _wrap_not_build_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._index is None:
            raise ValueError("Exec {} method, must run `build` method before.".format(func.__name__))
        return func(self, *args, **kwargs)
    return wrapper


class TopKSearch(object):

    __DEFAULT_FIF = "FIF"
    __DEFAULT_AOF = "AOF"
    __DEFAULT_BUFFER = "BUFFER"
    __DEFAULT_DUMPS_DIR = "data"
    __CMD_BUILD = "BUILD"
    __CMD_INSERT = "INSERT"
    __CMD_UPDATE = "UPDATE"
    __CMD_REMOVE = "REMOVE"

    def __init__(self,
                 data_dir: str,
                 version: str,
                 dim: int,
                 nlist: int = 128,
                 fif: str = None,
                 aof: str = None,
                 buffer: str = None,
                 dumps_dir: str = None):

        self._d = dim
        self._nlist = nlist
        self._data_dir = data_dir
        self._version = version
        self._dumps_dir = dumps_dir or self.__DEFAULT_DUMPS_DIR
        self._fif = fif or self.__DEFAULT_FIF
        self._aof = aof or self.__DEFAULT_AOF
        self._buffer = buffer or self.__DEFAULT_BUFFER

        self._aof_lock = False
        self._memory_lock = False
        self._index = None

        if not os.path.exists(self._data_dir):
            raise FileNotFoundError(self._data_dir)

        version_dir = os.path.join(self._data_dir, self._version)
        if not os.path.exists(version_dir):
            os.mkdir(version_dir)
            _dumps_data_dir = os.path.join(version_dir, self._dumps_dir)
            if not os.path.exists(_dumps_data_dir):
                os.mkdir(_dumps_data_dir)

    @property
    def aof_lock(self):
        return self._aof_lock

    @aof_lock.setter
    def aof_lock(self, lock: bool):
        self._aof_lock = lock

    @property
    def memory_lock(self):
        return self._memory_lock

    @memory_lock.setter
    def memory_lock(self, lock: bool):
        self._memory_lock = lock

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def num_total(self):
        if self._index is None:
            return 0
        return self._index.ntotal

    @property
    def dim(self):
        return self._d

    @property
    @_wrap_not_build_error
    def ids(self):
        index = core.extract_index_ivf(self._index)
        invlists = index.invlists
        all_ids = []
        for listno in range(index.nlist):
            ls = invlists.list_size(listno)
            if ls == 0:
                continue
            all_ids.append(
                core.rev_swig_ptr(invlists.get_ids(listno), ls).copy()
            )
        all_ids = np.hstack(all_ids)
        return all_ids

    @_warp_dtype_check("float32", "int64")
    def build(self, float32_vectors, int64_ids):

        if self._memory_lock is True and self._aof_lock is True:
            return self.write_aof(self.__CMD_BUILD, float32_vectors, int64_ids, buffer=True)

        if self._aof_lock is False:
            self.write_aof(self.__CMD_BUILD, float32_vectors, int64_ids)

        if self._memory_lock is False:
            quantizer = core.IndexFlatIP(self._d)

            self._index = core.IndexIVFFlat(quantizer,
                                            self._d,
                                            self._nlist,
                                            core.METRIC_INNER_PRODUCT)

            self._index.train(float32_vectors)
            self._index.add_with_ids(float32_vectors, int64_ids)

    @_wrap_not_build_error
    @_warp_dtype_check("float32", "int64")
    def insert(self, float32_vectors, int64_ids):

        if self._memory_lock is True and self._aof_lock is True:
            return self.write_aof(self.__CMD_INSERT, float32_vectors, int64_ids, buffer=True)

        if self._aof_lock is False:
            self.write_aof(self.__CMD_INSERT, float32_vectors, int64_ids)

        if self._memory_lock is False:
            self._index.add_with_ids(float32_vectors, int64_ids)

    @_wrap_not_build_error
    @_warp_dtype_check("float32", "int64")
    def update(self, float32_vectors, int64_ids):

        if self._memory_lock is True and self._aof_lock is True:
            return self.write_aof(self.__CMD_UPDATE, float32_vectors, int64_ids, buffer=True)

        if self._aof_lock is False:
            self.write_aof(self.__CMD_UPDATE, float32_vectors, int64_ids)

        if self._memory_lock is False:
            self._index.remove_ids(int64_ids)
            self._index.add_with_ids(float32_vectors, int64_ids)

    @_wrap_not_build_error
    @_warp_dtype_check("int64")
    def remove(self, int64_ids):

        if self._memory_lock is True and self._aof_lock is True:
            return self.write_aof(self.__CMD_REMOVE, int64_ids, buffer=True)

        if self._aof_lock is False:
            self.write_aof(self.__CMD_REMOVE, int64_ids)

        if self._memory_lock is False:
            self._index.remove_ids(int64_ids)

    @_wrap_not_build_error
    @_warp_dtype_check("float32")
    def search(self, float32_vectors, top_k: int = 10, nprobe: int = 10):
        self._index.nprobe = nprobe
        distances, ids = self._index.search(float32_vectors, top_k)
        return distances, ids

    @_wrap_not_build_error
    def save(self):
        _version_dir = os.path.join(self._data_dir, self._version)
        if not os.path.exists(_version_dir):
            os.mkdir(_version_dir)
        _fn = os.path.join(_version_dir, self._fif)
        core.write_index(self._index, _fn)

    def get_info(self):
        return {
            "num_total": self.num_total,
            "configs": {
                "dim": self.dim,
                "nlist": self._nlist,
                "data_dir": self._data_dir,
                "version": self._version,
                "dumps_dir": self._dumps_dir,
                "fif": self._fif,
                "aof": self._aof,
                "buffer": self._buffer,
            }
        }

    def rebuild(self):
        self.restore_from_fif()
        self.aof_lock = True
        self.restore_from_aof()
        self.aof_lock = False

    def restore_from_fif(self):
        _fn = os.path.join(self._data_dir, self._version, self._fif)
        if os.path.exists(_fn):
            self._index = core.read_index(_fn)

    def restore_from_aof(self, buffer=False):
        _aof = self._aof if buffer is False else self._buffer
        aof_path = os.path.join(self._data_dir, self._version, _aof)
        if os.path.exists(aof_path):
            with open(aof_path, "r") as f:
                for line in f:
                    args = line.strip("\n").split("\t")
                    cmd, paths = args[1], args[2:]
                    arrays = [self.loads_data(path) for path in paths]
                    ops = self.get_ops(cmd)
                    if ops is not None:
                        ops(*arrays)

    def write_aof(self, cmd, *arrays, buffer=False):
        _paths = []
        for array in arrays:
            fn = os.path.join(self._dumps_dir, self.get_random_filename() + ".npy")
            self.dumps_data(array, fn)
            _paths.append(fn)
        _aof = self._aof if buffer is False else self._buffer
        with open(os.path.join(self._data_dir, self._version, _aof), "a+") as f:
            f.write(self.get_strtime() + "\t" + cmd + "\t" + "\t".join(_paths) + "\n")

    def get_ops(self, cmd: str):

        _ops_map = {
            self.__CMD_BUILD: self.build,
            self.__CMD_INSERT: self.insert,
            self.__CMD_UPDATE: self.update,
            self.__CMD_REMOVE: self.remove
        }
        return _ops_map.get(cmd)

    def dumps_data(self, data, filename):
        _dumps_dir = os.path.join(self._data_dir, self._version, self._dumps_dir)
        if not os.path.exists(_dumps_dir):
            os.mkdir(_dumps_dir)
        np.save(os.path.join(self._data_dir, self._version, filename), data)

    def loads_data(self, filename):
        return np.load(os.path.join(self._data_dir, self._version, filename))

    @staticmethod
    def get_random_filename():
        return str(uuid.uuid4())

    @staticmethod
    def get_strtime(tz=None, fmt="%Y-%m-%d %H:%M:%S.%f"):
        return dt.datetime.now(tz=tz).strftime(fmt)

    def clear_buffer(self):
        _buffer = os.path.join(self._data_dir, self._version, self._buffer)
        if os.path.exists(_buffer):
            os.remove(_buffer)
