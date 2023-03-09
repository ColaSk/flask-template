# -*- coding: utf-8 -*-
import warnings
from flask import Flask
from flask_smorest import Api as _Api
from flask_smorest import Blueprint as _Blueprint
from marshmallow.exceptions import ValidationError
from webargs.flaskparser import FlaskParser
from werkzeug.exceptions import UnprocessableEntity

from configs.base import PROJECT_NAME
from utils.response import BaseResponse


warnings.simplefilter('ignore', UserWarning)


class Api(_Api):

    def _register_error_handlers(self):
        pass

    def add_spec_tag(self, *tag):
        for t in tag:
            self.spec.tag(t)


class Parser(FlaskParser):
    KNOWN_MULTI_FIELDS = []  # 减少 FlaskParser 自己会自己将 request.params 处理成List的问题

    # def _raw_load_json(self, req):
    #     """
    #     兼容不传ContentType的问题
    #     """
    #     return req.get_json(force=True)


class Blueprint(_Blueprint):
    ARGUMENTS_PARSER = Parser()
    TAGS = []

    def add_resource(self, resource, *urls):
        for url in urls:
            self.route(url)(resource)


smorest: Api


def _set_smorest(smorest_):
    global smorest
    smorest = smorest_


def get_smorest():
    global smorest
    return smorest

# TODO: 后续将UI迁移到本地，当前采用在线形式


def _set_swagger_doc(app: Flask):
    """设置openapi swagger"""
    if "OPENAPI_VERSION" not in app.config:
        app.config['OPENAPI_VERSION'] = '3.0.2'
    if "OPENAPI_URL_PREFIX" not in app.config:
        app.config['OPENAPI_URL_PREFIX'] = 'openapi'

    app.config['OPENAPI_SWAGGER_UI_PATH'] = 'swagger-doc'
    # app.config['OPENAPI_JSON_PATH'] = f'{BASE}/openapi.json'
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"


def _set_redoc(app: Flask):
    """设置openapi redoc"""
    if "OPENAPI_VERSION" not in app.config:
        app.config['OPENAPI_VERSION'] = '3.0.2'
    if "OPENAPI_URL_PREFIX" not in app.config:
        app.config['OPENAPI_URL_PREFIX'] = 'openapi'

    app.config["OPENAPI_REDOC_PATH"] = "/redoc"
    app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.30/bundles/redoc.standalone.js"


def init_smorest(app: Flask):

    app.config['API_TITLE'] = PROJECT_NAME
    app.config['API_VERSION'] = 'v1'
    app.config['JSON_AS_ASCII'] = False

    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['OPENAPI_URL_PREFIX'] = 'openapi'

    _set_swagger_doc(app)
    _set_redoc(app)

    @app.errorhandler(422)
    def c_422_handler(error: UnprocessableEntity):
        app.logger.debug(f"error message is {error.data['messages']}")
        return BaseResponse(
            message=" The request was well-formed but was unable to be followed due to semantic errors.",
            data=error.data['messages'],
            status=422,
            code=422,
        ).asdict()

    @app.errorhandler(ValidationError)
    def c_validate_handler(error: ValidationError):
        return BaseResponse(
            message=" The request was well-formed but was unable to be followed due to semantic errors.",
            data=error.messages,
            status=422,
            code=422,
        ).asdict()

    _set_smorest(Api(app))
