from functools import partial
from utils.exceptions import TipResponse
from initialization.jwtextend_process import auth as _auth
from initialization.jwtextend_process import CurrentUser


def _admin_auth_callback(curr_user):
    if not curr_user.is_admin:
        raise TipResponse('当前用户不是超级管理员')


auth = _auth
admin_auth = partial(_auth, callback=_admin_auth_callback)
