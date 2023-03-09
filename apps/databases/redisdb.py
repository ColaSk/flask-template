# -*- coding:utf-8 -*-
import redis as r
from redis.sentinel import Sentinel
from rediscluster import RedisCluster
from typing import Any
from abc import ABCMeta, abstractproperty
from threading import Lock


class RedisPool(r.ConnectionPool):
    """ redis 连接池
    1. 可以支持多db连接池
    """

    pools = {}
    pool_lock = Lock()

    def __new__(cls, *args, **kwargs):
        db = kwargs.get('db')
        with cls.pool_lock:
            if db in cls.pools:
                return cls.pools.get(db)
            obj = super().__new__(cls)
            cls.pools[db] = obj
            return obj


class RedisBase(object, metaclass=ABCMeta):
    """定义基础方法"""

    @abstractproperty
    def r(self): pass

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.r, __name)


class SingleRedisClinet(RedisBase):

    def __init__(self, pool_options: dict, db: int = 0, pool_class: RedisPool = RedisPool):
        self.db = db
        self.pool_options = pool_options
        self.pool_class = pool_class
        self._redis: r.Redis = None

    @property
    def r(self):
        if not self._redis:
            pool = self.pool_class(db=self.db, **self.pool_options)
            self._redis = r.Redis(connection_pool=pool)
        return self._redis


class SentinelRedisClient(Sentinel):
    """哨兵模式"""


class ClusterRedisClient(RedisCluster):
    """集群模式"""
