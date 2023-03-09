from flask import request

from utils.exceptions import NoAuthResponse, NoPermission, ParamResponse, TipResponse
from utils.response import BaseResponse
from flask import Flask


def init_exception(app: Flask):
    logger = app.logger

    @app.errorhandler(TipResponse)
    def tip_handler(error: TipResponse):
        """
        @attention: 提示
        """
        return BaseResponse(
            message=error.msg,
            status=error.status,
            code=error.code,
        ).asdict()

    @app.errorhandler(ParamResponse)
    def param_handler(error: ParamResponse):
        """
        @attention: 带参数提示
        """
        msg, data = error.show()
        return BaseResponse(200, 200, msg, data).asdict()

    @app.errorhandler(NoAuthResponse)
    def no_auth_response(error: NoAuthResponse):
        """
        处理登录发生的错误
        """
        return BaseResponse(
            message=error.msg,
            status=401,
            code=401,
        ).asdict()

    @app.errorhandler(NoPermission)
    def no_permission_response(error: NoPermission):
        """
        权限相关错误
        """
        return BaseResponse(message="无权限", status=403, code=403).asdict()

    @app.errorhandler(404)
    def c_404_handler(error):
        """
        @attention: 404服务器警告异常
        """
        return BaseResponse(message='Resource Not Found Error!', status=404, code=404).asdict()

    @app.errorhandler(400)
    def c_400_handler(error):
        """
        @attention: 400服务器警告异常
        """
        return BaseResponse(message='Bad request!', status=400, code=400).asdict()

    @app.errorhandler(405)
    def c_405_handler(error):
        """
        @attention: 405服务器警告异常
        """
        return BaseResponse(
            message='The method is not allowed for the requested URL!',
            status=405,
            code=405,
        ).asdict()

    @app.errorhandler(500)
    def c_500_handler(error):
        """
        @attention: 500服务器警告异常
        """
        return BaseResponse(
            message='System Error!',
            status=500,
            code=500,
        ).asdict()

    @app.errorhandler(Exception)
    def base_handler(error):
        """
        @attention: 未知异常
        """
        url_data = "url(%s):%s" % (request.url, request.method)
        get_data = "get_data:%s" % dict(request.args)
        json_data = "json_data:%s" % request.params
        log_msg = "\n".join([url_data, get_data, json_data])
        logger.error(log_msg)
        logger.exception(error)
        msg = "系统繁忙，请稍后再试!"
        return BaseResponse(code=500, message=msg, status=500).asdict()
