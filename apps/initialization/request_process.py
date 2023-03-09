"""
拓展flask的self
"""

from flask import request, Response, Flask
from flask.wrappers import Request as _Request

from utils.common_tools import get_request_id


class Request(_Request):

    @property
    def request_id(self):
        if self._request_id:
            return self._request_id

        request_id = self.headers.get("Request-ID")
        if not request_id:
            request_id = get_request_id()

        self._request_id = request_id
        return self._request_id

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._request_id = None
        self._param = None

    @property
    def params(self):
        """
        根据不同类型的请求去获取对应的data
        POST, PUT -> request.data or request.form
        GET, DELETE -> request.args
        """
        if self._param is not None:
            return self._param

        data = {}
        if self.method in ("POST", "PUT"):
            data = self.get_json(force=True) if self.data.strip() else {k: v for k, v in self.form.items()}
        elif self.method in ("DELETE", "GET"):
            data = self.args
        self._param = data
        return data


def init_request(app: Flask):

    app.request_class = Request

    @app.before_request
    def log_before_request():
        """打印入参"""
        app.logger.info(f"request-id: <{request.request_id}> request start".center(100, '*'))
        app.logger.info(f"request-id: <{request.request_id}> params: {request.params}")

    @app.after_request
    def cors_after_request(response: Response):
        """跨域设置"""

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Method'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Request-Private-Network'] = True
        return response

    @app.after_request
    def log_after_request(response: Response):
        """log"""
        app.logger.info(f"request-id: <{request.request_id}> request end".center(100, '*'))
        return response
