from typing import Any
from functools import wraps
from flask import Flask, current_app
from flask_jwt_extended import JWTManager as _JWTManager
from flask_jwt_extended import current_user, verify_jwt_in_request, create_access_token
from flask_jwt_extended import get_jwt as get_jwt_extended
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError
from configs.base import SECRET_KEY
from configs.sysconf import JWT_ACCESS_TOKEN_EXPIRES
from utils.response import BaseResponse
from utils.exceptions import TipResponse
from utils.datetime_tools import get_current_timestamp
from .redis_process import RedisExtension


class JWTManager(_JWTManager):

    def init_app(self, app):
        super().init_app(app)
        self.app = app

    def _set_error_handler_callbacks(self, app):
        """
        暂停注册错误, 由exception_process统一处理
        """
        ...


class AnonymousUser:
    """
    有别于登录的用户
    """

    is_superuser = False
    is_anonymous = True

    def __getattribute__(self, name: str) -> Any:
        if name in ('is_superuser', "is_anonymous"):
            return super().__getattribute__(name)
        return None


jwt: JWTManager


def set_jwt(_jwt: JWTManager):
    global jwt
    jwt = _jwt


def get_jwt():
    global jwt
    return jwt


def init_jwt(app: Flask):

    app.config['JWT_SECRET_KEY'] = SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]

    jwt = JWTManager(app)
    set_jwt(jwt)

    @jwt.user_identity_loader
    def user_identity_loader_callback(user):
        return dict(
            id=user.id,
            username=user.username,
            userlevel=user.userlevel,
            is_admin=user.is_admin
        )

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        """存储附加数据
        """
        _additional_claims = dict(
            login_time=get_current_timestamp(by_sc=True)
        )
        return _additional_claims

    @jwt.user_lookup_loader
    def user_loader_callback(_jwt_header, jwt_data):
        """自动加载用户"""
        from models.models import UserModel
        from models.utils import check_object_exist

        userinfo = jwt_data.get("sub")
        if not userinfo:
            raise JWTExtendedException("Invalid Token!")

        id = userinfo.get('id')
        try:
            user = check_object_exist(UserModel, id)
        except TipResponse:
            raise JWTExtendedException("Invalid Token!")

        return user

    @jwt.token_in_blocklist_loader
    def check_token_revoked(jwt_header, jwt_payload: dict):
        """检查token是否被撤销
        """
        token_manager = TokenManager()
        jti = jwt_payload["jti"]

        return token_manager.check_token_revoked(jti)

    @app.errorhandler(JWTExtendedException)
    def no_auth_handler(error: JWTExtendedException):
        """
        @attention: 提示
        """

        jwt_header = getattr(error, 'jwt_header', None)
        jwt_data = getattr(error, 'jwt_data', None)

        def err_format(err_str, jwt_header, jwt_data):

            return str(dict(
                jwt_header=jwt_header,
                jwt_data=jwt_data,
                error=err_str
            ))

        err = err_format(str(error), jwt_header, jwt_data)

        app.logger.debug(f"error message is {err}")

        return BaseResponse(
            message=str(error),
            status=401,
            code=401,
        ).asdict(), 401

    @app.errorhandler(PyJWTError)
    def jwt_err_hander(error: PyJWTError):

        app.logger.debug(f"error message is {error}")

        return BaseResponse(
            message=str(error),
            status=401,
            code=401,
        ).asdict(), 401


def auth(optional=False, fresh=False, refresh=False, locations=None, callback=None):

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(optional, fresh, refresh, locations)

            # 回调处理函数
            if callback:
                callback(current_user)

            # Compatibility with flask < 2.0
            if hasattr(current_app, "ensure_sync") and callable(
                getattr(current_app, "ensure_sync", None)
            ):
                return current_app.ensure_sync(fn)(*args, **kwargs)

            return fn(*args, **kwargs)  # pragma: no cover

        return decorator
    return wrapper


class CurrentUser(object):

    def __init__(self, user=None):
        """
        user: models.models.UserModel
        """

        if user:
            self.user = user
        else:
            self.user = current_user

    def get_jwt(self):
        """获取当前用户的jwt"""
        jwt_ = get_jwt_extended()
        return jwt_

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.user, __name)


class TokenManager(object):

    """token 管理器
    1. 生成
    2. 撤销
    3. 验证
    """

    def __init__(self, redis_extension: RedisExtension = None):

        # 无伤获取redis服务
        if not redis_extension:
            redis_client = jwt.app.extensions.get('redis_client')
            if not redis_client:
                raise TipResponse("当前不存在redis_client,需要检查!!!", 500, 500)
            redis_extension = redis_client
        self.r = redis_extension

    @property
    def redis_client(self):
        return self.r.r

    def create_access_token(self, identity, additional_claims: dict = None):
        """创建token"""

        token = create_access_token(identity, additional_claims=additional_claims)
        return token

    def revoke_token(self):
        """撤销token
        设置一个标志,指代当前token已被撤销
        """
        jti = get_jwt_extended()["jti"]
        self.redis_client.set(jti, "", ex=JWT_ACCESS_TOKEN_EXPIRES)

    def check_token_revoked(self, jti):
        """验证token撤销"""
        token = self.redis_client.get(jti)
        return token is not None
