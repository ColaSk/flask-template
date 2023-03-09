from flask import Flask

from configs import base
from configs import sysconf

from .logger_process import init_logger
from .sqlalchemy_process import init_db
from .smorest_process import init_smorest
from .schema_process import init_marshmallow_errorhandler
from .request_process import init_request
from .blueprint_process import init_smorest_blueprint
from .service_process import init_service
from .exception_process import init_exception
from .command_process import init_command
from .sqlalchemy_models_process import init_sqlalchemy_models
from .redis_process import init_redis
from .jwtextend_process import init_jwt

app: Flask


def _init(app: Flask):
    """新的初始化方法
    """
    init_logger(app)
    init_exception(app)
    init_db(app)
    init_sqlalchemy_models()
    init_redis(app)
    init_command(app)
    init_service(app)
    init_smorest(app)
    init_smorest_blueprint(app)
    init_marshmallow_errorhandler(app)
    init_request(app)
    init_jwt(app)


def create_app() -> Flask:
    global app

    app = Flask(
        base.PROJECT_NAME,
        static_url_path=sysconf.STATIC_URL_PATH,
        static_folder=sysconf.STATIC_FOLDER)

    _init(app)

    return app


def get_app() -> Flask:
    global app
    return app
