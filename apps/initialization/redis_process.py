import copy
from typing import Any
from flask import Flask
from configs import sysconf as conf
from databases.redisdb import SingleRedisClinet


class RedisExtension(object):

    def __init__(self, redis, type: str):
        self.redis = redis
        self.type = type

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.redis, __name)


def init_redis(app: Flask):
    """初始化redis服务"""
    logger = app.logger
    config = conf.REDIS_CONFIG

    redis_type = config.pop('type', 'single')

    if redis_type == 'single':
        db = config.pop('db', 0)
        pool_options = copy.deepcopy(config)
        redis_exrension = RedisExtension(
            SingleRedisClinet(pool_options, db), redis_type)
        app.extensions["redis_client"] = redis_exrension
    else:
        logger.error("redis 不支持此类型")
