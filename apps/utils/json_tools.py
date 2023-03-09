from typing import Any

from initialization.logger_process import logger

json = None


def get_json_import():
    """
    依次引入Json序列化器
    """
    global json
    try:
        import ujson
        json = ujson
        return
    except ImportError:
        pass

    try:
        import simplejson
        json = simplejson
        return
    except ImportError:
        pass

    import json
    json = json


get_json_import()


def json_loads(json_str: str, need_raise: bool = False) -> dict:
    """
    安全的加载一个json字符串, 及时失败了, 任然返回空字典
    """
    if not json_str or not isinstance(json_str, (str, bytearray, bytes)):
        return dict()
    try:
        return json.loads(json_str)
    except Exception as e:
        logger.exception(e)
        if need_raise:
            raise e
        return dict()


def json_dumps(json_obj: Any, need_raise: bool = False) -> str:
    """
    安全得dump一个字典, 及时报错了仍然返回空字符串
    """
    try:
        return json.dumps(json_obj, ensure_ascii=False)
    except Exception as e:
        logger.exception(e)
        if need_raise:
            raise e
        return ""
