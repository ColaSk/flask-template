# -*- coding: utf-8 -*-
from libs import set_logger, ServiceException
from utils.response import BaseResponse
from flask import Flask


def init_service(app: Flask):

    set_logger(app.logger)

    @app.errorhandler(ServiceException)
    def service_exception(e: ServiceException):
        return BaseResponse(
            message=f"third party service is unavailable right now, error: {e}",
            code=500,
            status=500).asdict()
