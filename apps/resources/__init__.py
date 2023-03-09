from initialization.smorest_process import Blueprint

BPS = []


def get_bps():
    global BPS
    return BPS


def create_blueprint(*args, **kwargs):
    global BPS
    bp = Blueprint(*args, **kwargs)
    BPS.append(bp)
    return bp


basic_bp_v1 = create_blueprint("基础[Basic]", 'basic_bp_v1')


from . import basic
