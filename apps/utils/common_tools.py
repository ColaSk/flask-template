# coding:utf-8
import os
import uuid
import hashlib

from .datetime_tools import get_current_timestamp


def get_md5(string: str):
    """获取字符串md5的值"""
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    digest = md5.hexdigest()
    return digest


def safe_split(pre_str, sepdot, seprelates):
    for s in seprelates:
        pre_str = pre_str.replace(s, sepdot)
    return pre_str.split(sepdot)


def sage_split_by_comma(pre_str):
    pre_str = str(pre_str)
    return safe_split(pre_str, sepdot=",", seprelates=[",", "，"])


def file_name_generator(file_name):
    subfix = os.path.splitext(file_name)[-1]
    return "%s%s" % (str(uuid.uuid4()), subfix)


def generate_uuid_filename(subfix):
    return "%s%s" % (str(uuid.uuid4()), subfix)


def replace_file_subfix(file_name, subfix):
    return os.path.splitext(file_name)[0] + subfix


def get_uuid(prefix="", subfix=""):
    return "%s%s%s" % (prefix, str(uuid.uuid4()), subfix)


def get_request_id():
    return get_current_timestamp(by_ms=True)


def parse_query_range(query_str):
    """
    根据查询的区间，返回区间的两端的值。
    @param query_str  eg: 2019TO2020 return 2019, 2010
    """
    if not query_str or str(query_str).strip().upper() in ("NULL", "NONE"):
        return None, None
    if not query_str or "TO" not in query_str or len(str(query_str).split("TO")) != 2:
        return query_str, query_str
    query_str = str(query_str).replace("[", "").replace("]", "").replace(")", "").replace("(", "")
    left_val, right_val = query_str.split("TO")
    return left_val.strip(), right_val.strip()


def parse_ids_from_str(ids_str, allow_duplicate=False, sep=','):
    """
    从String 中解析ID，
    @params id_str eg: "112, 113,114"
    @params allow_duplicate 是否允许重复
    @return id str list eg: [112, 113, 114]
    """
    if not ids_str:
        return []
    if not isinstance(ids_str, str):
        return ids_str
    if not ids_str or not str(ids_str).strip():
        return []
    id_list = [i for i in str(ids_str).split(sep) if i.strip()]
    return id_list if allow_duplicate else list(set(id_list))


def add_unhashable_obj_without_duplicate(obj_list, objs, key_getter, obj_keys=None):
    """
    将某个某个对象放入不重复的列表中, 适合不能被哈希的对象, 无法放入set中进行去重
    该方法会原地修改obj_list与obj_keys
    :param obj_list     要素列表
    :param objs         需要添加的要素
    :param key_getter   用来获取source中的key(要求key可哈希), 一般情况下是itemgetter, 或者是attrgetter
    :type  key_getter   function(Any) -> Hashable
    :param obj_keys     用来去重的集合, 如果不传入, 将每次都会遍历obj_list
    :type obj_keys      set
    >>> res = [dict(key=1)]
    >>> add_unhashable_obj_without_duplicate(res, [dict(key=1)], itemgetter("key"))
    [{'key': 1}]
    """
    if obj_keys is not None:
        for obj in objs:
            _key = key_getter(obj)
            if _key in obj_keys:
                continue
            obj_list.append(obj)
            obj_keys.add(_key)
    else:
        for obj in objs:
            _key = key_getter(obj)
            if _key in (key_getter(o) for o in obj_list):
                continue
            obj_list.append(obj)

    return obj_list


if __name__ == "__main__":
    pass
