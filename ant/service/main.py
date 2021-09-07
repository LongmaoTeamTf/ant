#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import shutil
import uvicorn
import requests
import numpy as np
from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler

from ant.core import TopKSearch
from ant.core import MultiInstances
from ant.core import OPS
from ant.service import ConfigFlags
from ant.service import Status
from ant.service import AntAPIs
from ant.service import AntResponse
from ant.logger import AntLogger
from ant.logger.wrappers import timing
from ant.logger.wrappers import catch_exception


config_flags = ConfigFlags()
app = FastAPI()
scheduler = BackgroundScheduler(timezone=config_flags.logger.meta.tz)
mis = MultiInstances(config_flags.service.multi_instances.data_dir)

logger = AntLogger(**config_flags.logger.meta.dict)(config_flags.logger.handlers.dict)


@app.get(AntAPIs.LIST.path)
@catch_exception(AntAPIs.LIST.path, logger=logger)
@timing()
def list_instances():
    resp = mis.list_instances()
    return AntResponse(Status.SUCCESS, api=AntAPIs.LIST.path, ops=OPS.LIST, result=resp)


@app.post(AntAPIs.CREATE.path)
@catch_exception(AntAPIs.CREATE.path, logger=logger)
@timing()
def create(params: AntAPIs.CREATE.params):
    instance_name = params.instance_name
    configs = params.configs
    mis.create_instance(instance_name, configs)
    return AntResponse(Status.SUCCESS, api=AntAPIs.CREATE.path, ops=OPS.CREATE, instance=instance_name)


@app.post(AntAPIs.DELETE.path)
@catch_exception(AntAPIs.DELETE.path, logger=logger)
@timing()
def delete(params: AntAPIs.DELETE.params):
    instance_name = params.instance_name
    if instance_name not in mis.list_instances():
        raise ValueError("Instance `{}` is not exist.".format(instance_name))
    mis.delete_instance(instance_name)
    return AntResponse(Status.SUCCESS, api=AntAPIs.DELETE.path, ops=OPS.DELETE, instance=instance_name)


@app.post(AntAPIs.BUILD.path)
@catch_exception(AntAPIs.BUILD.path, logger=logger)
@timing()
def build(params: AntAPIs.BUILD.params):
    instance_name = params.instance_name
    vectors = params.vectors
    ids = params.ids
    mode = params.mode

    if instance_name not in mis.list_instances():
        raise ValueError("Instance `{}` is not exist.".format(instance_name))

    if mode not in ("list", "npy"):
        msg = "`{}` not supported, `mode` param should be in ('list', 'npy')".format(mode)
        raise ValueError(msg)

    if mode == "list" and (isinstance(vectors, str) or isinstance(ids, str)):
        msg = "When `mode` = `list`, the `vectors` and `ids` must be list."
        raise ValueError(msg)

    if mode == "npy" and (isinstance(vectors, list) or isinstance(ids, list)):
        msg = "When `mode` = `npy`, the `vectors` and `ids` must be string."
        raise ValueError(msg)

    if mode == "npy":
        vectors = np.load(vectors)
        ids = np.load(ids)
    instance = mis.get_instance(instance_name)

    if instance.dim != vectors.shape[-1]:
        raise ValueError("Faiss instance's dim = {}, vectors's dim = {}, not match!".format(
            instance.dim, vectors.shape[-1]))

    instance.build(vectors, ids)
    return AntResponse(Status.SUCCESS, api=AntAPIs.BUILD.path, ops=OPS.BUILD, instance=instance_name)


@app.post(AntAPIs.INSERT.path)
@catch_exception(AntAPIs.INSERT.path, logger=logger)
@timing()
def insert(params: AntAPIs.INSERT.params):
    instance_name = params.instance_name
    vectors = params.vectors
    ids = params.ids
    mode = params.mode

    if instance_name not in mis.list_instances():
        raise ValueError("Instance `{}` is not exist.".format(instance_name))

    if mode not in ("list", "npy"):
        msg = "`{}` not supported, `mode` param should be in ('list', 'npy')".format(mode)
        raise ValueError(msg)

    if mode == "list" and (isinstance(vectors, str) or isinstance(ids, str)):
        msg = "When `mode` = `list`, the `vectors` and `ids` must be list."
        raise ValueError(msg)

    if mode == "npy" and (isinstance(vectors, list) or isinstance(ids, list)):
        msg = "When `mode` = `npy`, the `vectors` and `ids` must be string."
        raise ValueError(msg)

    if mode == "npy":
        vectors = np.load(vectors)
        ids = np.load(ids)
    instance = mis.get_instance(instance_name)

    if instance.dim != vectors.shape[-1]:
        raise ValueError("Faiss instance's dim = {}, vectors's dim = {}, not match!".format(
            instance.dim, vectors.shape[-1]))

    instance.insert(vectors, ids)
    return AntResponse(Status.SUCCESS, api=AntAPIs.INSERT.path, ops=OPS.INSERT, instance=instance_name)


@app.post(AntAPIs.UPDATE.path)
@catch_exception(AntAPIs.UPDATE.path, logger=logger)
@timing()
def update(params: AntAPIs.UPDATE.params):
    instance_name = params.instance_name
    vectors = params.vectors
    ids = params.ids
    mode = params.mode

    if instance_name not in mis.list_instances():
        raise ValueError("Instance `{}` is not exist.".format(instance_name))

    if mode not in ("list", "npy"):
        msg = "`{}` not supported, `mode` param should be in ('list', 'npy')".format(mode)
        raise ValueError(msg)

    if mode == "list" and (isinstance(vectors, str) or isinstance(ids, str)):
        msg = "When `mode` = `list`, the `vectors` and `ids` must be list."
        raise ValueError(msg)

    if mode == "npy" and (isinstance(vectors, list) or isinstance(ids, list)):
        msg = "When `mode` = `npy`, the `vectors` and `ids` must be string."
        raise ValueError(msg)

    if mode == "npy":
        vectors = np.load(vectors)
        ids = np.load(ids)
    instance = mis.get_instance(instance_name)

    if instance.dim != vectors.shape[-1]:
        raise ValueError("Faiss instance's dim = {}, vectors's dim = {}, not match!".format(
            instance.dim, vectors.shape[-1]))

    instance.update(vectors, ids)
    return AntResponse(Status.SUCCESS, api=AntAPIs.UPDATE.path, ops=OPS.UPDATE, instance=instance_name)


@app.post(AntAPIs.REMOVE.path)
@catch_exception(AntAPIs.REMOVE.path, logger=logger)
@timing()
def remove(params: AntAPIs.REMOVE.params):
    instance_name = params.instance_name
    ids = params.ids
    mode = params.mode

    if instance_name not in mis.list_instances():
        raise ValueError("Instance `{}` is not exist.".format(instance_name))

    if mode not in ("list", "npy"):
        msg = "`{}` not supported, `mode` param should be in ('list', 'npy')".format(mode)
        raise ValueError(msg)

    if mode == "list" and isinstance(ids, str):
        msg = "When `mode` = `list`, the `ids` must be list."
        raise ValueError(msg)

    if mode == "npy" and isinstance(ids, list):
        msg = "When `mode` = `npy`, the `ids` must be string."
        raise ValueError(msg)

    if mode == "npy":
        ids = np.load(ids)
    instance = mis.get_instance(instance_name)

    if isinstance(ids, np.ndarray):
        ids = ids.tolist()

    remove_ids = list(set(ids) & set(instance.ids))

    instance.remove(remove_ids)
    return AntResponse(Status.SUCCESS, api=AntAPIs.REMOVE.path, ops=OPS.REMOVE, instance=instance_name)


@app.post(AntAPIs.SEARCH.path)
@catch_exception(AntAPIs.SEARCH.path, logger=logger)
@timing()
def search(params: AntAPIs.SEARCH.params):
    instance_name = params.instance_name
    vectors = params.vectors
    top_k = params.top_k
    nprobe = params.nprobe

    if instance_name not in mis.list_instances():
        raise ValueError("Instance `{}` is not exist.".format(instance_name))

    instance = mis.get_instance(instance_name)

    if instance.dim != np.asarray(vectors).shape[-1]:
        raise ValueError("Faiss instance's dim = {}, vectors's dim = {}, not match!".format(
            instance.dim, np.asarray(vectors).shape[-1]))

    distances, ids = instance.search(vectors, top_k=top_k, nprobe=nprobe)

    result = [dict(zip(_ids, _distances)) for _ids, _distances in zip(ids.tolist(), distances.tolist())]
    return AntResponse(Status.SUCCESS, api=AntAPIs.SEARCH.path, ops=OPS.SEARCH, instance=instance_name, result=result)


@app.post(AntAPIs.INFO.path)
@catch_exception(AntAPIs.INFO.path, logger=logger)
@timing()
def get_instance_info(params: AntAPIs.INFO.params):
    instance_name = params.instance_name
    if instance_name not in mis.list_instances():
        raise ValueError("Instance `{}` is not exist.".format(instance_name))
    instance = mis.get_instance(instance_name)
    info = instance.get_info()
    return AntResponse(Status.SUCCESS, api=AntAPIs.INFO.path, ops=OPS.INFO, instance=instance_name, result=info)


@catch_exception("backup", logger=logger)
def instance_backup(instance_name):
    instance = mis.get_instance(instance_name)
    instance.memory_lock = True
    instance.aof_lock = True
    instance.version = TopKSearch.get_strtime(fmt="%Y%m%d%H%M%S%f")
    instance.save()
    instance.memory_lock = False
    instance.aof_lock = False
    instance.restore_from_aof(buffer=True)
    instance.clear_buffer()
    mis.update_instance_version(instance_name, instance.version)
    mis.save_instance_conf(instance_name)
    msg = "`{}` backup completed.".format(instance_name)
    return AntResponse(Status.SUCCESS, api=AntAPIs.BGSAVE.path, instance=instance_name, msg=msg)


@app.post(AntAPIs.BGSAVE.path + "/{instance_name}")
@catch_exception(AntAPIs.BGSAVE.path, logger=logger)
def bgsave(instance_name: str, background_tasks: BackgroundTasks):
    msg = "Instance `{}` background backup.".format(instance_name)
    if instance_name not in mis.list_instances():
        raise ValueError("Instance `{}` is not exist.".format(instance_name))
    background_tasks.add_task(instance_backup, instance_name)
    return AntResponse(Status.SUCCESS, api=AntAPIs.BGSAVE.path, instance=instance_name, msg=msg)


@scheduler.scheduled_job("interval", hours=config_flags.service.scheduler.backup.hours)
def scheduler_backup():
    for instance in mis.list_instances():
        url = f"http://localhost:{config_flags.service.port}/{AntAPIs.BGSAVE.path}/{instance}"
        resp = requests.post(url)
        logger.info(resp)


@scheduler.scheduled_job("interval", hours=config_flags.service.scheduler.clear_backup.hours)
def scheduler_clear_backup(max_keep_backups=config_flags.service.scheduler.clear_backup.max_keep_backups):
    for instance in mis.list_instances():
        backup_dir = os.path.join(mis.member_dir, instance)
        objs = os.listdir(backup_dir)
        versions = []
        for obj in objs:
            if os.path.isfile(obj):
                continue
            versions.append(obj)

        remove_versions = sorted(versions, reverse=True)[max_keep_backups:]

        for version in remove_versions:
            version_dir = os.path.join(backup_dir, version)
            shutil.rmtree(version_dir)

        logger.info(AntResponse(Status.SUCCESS, instance=instance, msg="clear backup"))


if __name__ == "__main__":
    scheduler.start()
    uvicorn.run(app="main:app",
                host=config_flags.service.uvicorn.host,
                port=config_flags.service.uvicorn.port,
                reload=config_flags.service.uvicorn.reload,
                debug=config_flags.service.uvicorn.debug,
                workers=config_flags.service.uvicorn.workers)
