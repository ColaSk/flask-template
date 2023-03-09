from resources import get_bps
from initialization.smorest_process import get_smorest, init_smorest
from flask import Flask


def init_smorest_blueprint(app: Flask):
    smorest = get_smorest()
    if not smorest:
        init_smorest(app)
        smorest = get_smorest()

    for bp in get_bps():
        smorest.register_blueprint(bp, url_prefix='/v1')
