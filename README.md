# Ant
[![python](https://img.shields.io/badge/python-3.7-brightgreen)](requirements.txt)
[![faiss_cpu](https://img.shields.io/badge/faiss_cpu-1.6-brightgreen)](requirements.txt)
[![license](https://img.shields.io/badge/license-Apache_2.0-green)](LICENSE)
[![test](https://img.shields.io/badge/test-passing-brightgreen)]()

Ant is an open-source vector database built to embedding similarity search based on [Faiss](https://github.com/facebookresearch/faiss).
Data backup draws on the hybrid mechanism of Redis's RDB and AOF to ensure data security and consistency.

## Quick start
*Build docker image.*
```shell script
$ docker build -t ant:latest .
```
*Start ant server.*
```shell script
$ docker run ant:latest -p 1234:1234 -v {logs_dir}:/ant/logs {data_dir}:/ant/data
```

## Restful API

| Method | URL | description | Status |
| ------ | --- | ----------- | ------ | 
| POST | [/ant/create](RestfulAPI.md#创建实例)   | *Create the instance by name.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |
| POST | [/ant/delete](RestfulAPI.md#删除实例)   | *Delete the instance by name.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |
| GET  | [/ant/list](RestfulAPI.md#列举实例)     | *List all instances.* | [![](https://img.shields.io/badge/passing-brightgreen)]() |
| POST | [/ant/info](RestfulAPI.md#获取实例信息)  | *Get the information of instance by name.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |
| POST | [/ant/build](RestfulAPI.md#构建索引)    | *Build the Faiss index of instance by input data.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |
| POST | [/ant/insert](RestfulAPI.md#插入索引数据) | *Insert data to Faiss index of instance.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |
| POST | [/ant/update](RestfulAPI.md#更新索引数据) | *Update the Faiss index of instance.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |
| POST | [/ant/remove](RestfulAPI.md#删除索引数据) | *Remove data of the Faiss index of instance.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |
| POST | [/ant/search](RestfulAPI.md#K近邻查询) | *K-nearest neighbor query from Faiss index.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |
| GET  | [/ant/bgsave](RestfulAPI.md#后台备份) | *Back up index data in the background.*| [![](https://img.shields.io/badge/passing-brightgreen)]() |

## Configuration
* [Logger](ant/configs/logger.yml)
* [Service](ant/configs/service.yml)

## License
[Apache-2.0](ant/LICENSE)