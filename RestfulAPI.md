# Restful API

## 创建实例
- Method: **POST**
- URL: ```/ant/create```
- Headers：```application/json```
- Body: 
```
{
    "instance_name": "{instance_name}",
    "configs": {
        "dim": int,
        "nlist": int
    }
}
```

## 删除实例
- Method: **POST**
- URL: ```/ant/delete```
- Headers：```application/json```
- Body: 
```
{
    "instance_name": "{instance_name}"
}
```

## 列举实例
- Method: **GET**
- URL: ```/ant/list```
- Headers：```null```
- Body: ```null```


## 获取实例信息
- Method: **POST**
- URL: ```/ant/info```
- Headers：```application/json```
- Body: 
```
{
    "instance_name": "{instance_name}"
}
```

## 构建索引
- Method: **POST**
- URL: ```/ant/build```
- Headers：```application/json```
- Body: 
```
{
    "instance_name": "{instance_name}", 
    "vectors": "{filepath}" | list | array, 
    "ids": "{filepath}" | list | array, 
    "mode": "npy" | "array"
}
```

## 插入索引数据
- Method: **POST**
- URL: ```/ant/insert```
- Headers：```application/json```
- Body: 
```
{
    "instance_name": "{instance_name}", 
    "vectors": "{filepath}" | list | array, 
    "ids": "{filepath}" | list | array, 
    "mode": "npy" | "array"
}
```

## 更新索引数据
- Method: **POST**
- URL: ```/ant/update```
- Headers：```application/json```
- Body: 
```
{
    "instance_name": "{instance_name}", 
    "vectors": "{filepath}" | list | array, 
    "ids": "{filepath}" | list | array, 
    "mode": "npy" | "array"
}
```

## 删除索引数据
- Method: **POST**
- URL: ```/ant/remove```
- Headers：```application/json```
- Body: 
```
{
    "instance_name": "{instance_name}", 
    "ids": "{filepath}" | list | array, 
    "mode": "npy" | "array"
}
```

## K近邻查询
- Method: **POST**
- URL: ```/ant/search```
- Headers：```application/json```
- Body: 
```
{
    "instance_name": "{instance_name}", 
    "vectors": list | array, 
    "top_k": int,
    "nprobe": int
}
```

## 后台备份
- Method: **GET**
- URL: ```/ant/bgsave/{instance_name}```
- Headers：```null```
- Body: ```null```
