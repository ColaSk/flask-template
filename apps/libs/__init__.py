# -*- coding: utf-8 -*-
import logging
from functools import wraps
from logging import getLogger
from reprlib import repr
from time import sleep

import requests

logger = getLogger("service")
logger.setLevel("INFO")
logger.handlers.append(logging.StreamHandler())


def set_logger(_logger):
    global logger
    logger = _logger


def retry(times: int):
    """
    使得一个任务重试
    :param times 重试次数
    """

    def outter(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"func {func.__name__} failed {i + 1} rd time, will try {times} times")
                    logger.exception(e)

                    sleep(1)
                    # 次数到了则抛出异常
                    if i == times - 1:
                        raise e

        return wrapper

    return outter


class BaseClient:

    def __init__(self, host, port=None, timeout=(3, 30)):
        self.host = host
        self.port = port
        self.session = requests.session()
        self.timeout = timeout

    @property
    def url(self):
        if self.port:
            return f"http://{self.host}:{self.port}"
        return f"http://{self.host}"

    @retry(3)
    def _post(self, api, **kwargs):
        return self._request_wrapper("post", api, **kwargs)

    @retry(3)
    def _get(self, api, **kwargs):
        return self._request_wrapper("get", api, **kwargs)

    @retry(3)
    def _put(self, api, **kwargs):
        return self._request_wrapper("put", api, **kwargs)

    @retry(3)
    def _delete(self, api, **kwargs):
        return self._request_wrapper("delete", api, **kwargs)

    def _request_wrapper(self, method, api, **kwargs):
        logger.info(f"sending {method} request to {self.url + api} ...  kwargs is {repr(kwargs)}")
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        res = self.session.request(method, self.url + api, **kwargs)

        if res.status_code != 200:
            raise ServiceException(f"Http status code is not 200, status code {res.status_code}, "
                                   f"response is {res.content}")

        logger.info(f"sending {method} request to {self.url + api} over ... response is "
                    f"{res.text}")
        return res

    def __del__(self):
        try:
            if hasattr(self, "session"):
                self.session.close()
        except Exception as e:
            logger.exception(e)


class FlaskClient(BaseClient):

    def _request_wrapper(self, method, api, **kwargs):
        from flask import request
        headers = kwargs.setdefault("headers", dict())
        headers['Request-ID'] = request.request_id
        return super()._request_wrapper(method, api, **kwargs)


class ServiceException(Exception):
    ...
