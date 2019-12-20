# -*- coding: utf-8 -*-
# @Time    : 2019/10/26 13:25
# @Author  : CRJ
# @File    : conn.py
# @Software: PyCharm
# @Python3.6
"""
    提供redis、mysql等连接对象实例

"""
import redis
from .settings import *
import pika

# 从redis连接池中获取连接对象
redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, max_connections=512)
redis_conn = redis.Redis(connection_pool=redis_pool)


# 创建rabbitmq连接
rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))

"""
show variables like 'max_connections'; 查看数据库最大连接数

set global max_connections=1000  修改

"""