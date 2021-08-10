#!/usr/bin/python3
# -*- coding: utf-8 -*-
from functools import wraps

import time
from ant.service import AntResponse, Status


def timing():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            resp = func(*args, **kwargs)
            stop_time = time.time()
            resp.add_attrs(time=round(stop_time - start_time, 4)*1000)
            return resp
        return wrapper
    return decorator


def catch_exception(api, logger=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                resp = func(*args, **kwargs)
                if logger is not None:
                    logger.info(resp)
            except Exception as e:
                resp = AntResponse(Status.ERROR, api=api, error=repr(e))
                if logger is not None:
                    logger.error(resp)
            return resp
        return wrapper
    return decorator
