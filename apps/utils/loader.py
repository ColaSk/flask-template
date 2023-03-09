import os
from typing import Optional

conf_dict = {}


def load_from_file(file_path=None) -> dict:
    '''
    @param file_path
    从配置文件中加载配置
    '''
    file_path = file_path or env_loader('GLOBAL_CONF_PATH') or "/run/secrets/global.conf"
    if os.path.exists(file_path):
        with open(file_path) as infile:
            for line in infile:
                if not line.strip() or line.strip().startswith("#") or '=' not in line:
                    continue
                tlist = line.strip().split('=')
                if len(tlist) != 2:
                    continue
                key, val = tlist
                # 支持多个值
                vals = val.split(',')
                if len(vals) > 1:
                    val = [v for v in vals if v]
                conf_dict[key.upper()] = val
    return conf_dict


def file_loader(key):
    if not conf_dict:
        load_from_file()
    return conf_dict[key] if key in conf_dict else None


def env_loader(key) -> Optional[str]:
    '''
    从环境变量中加载
    '''
    return os.environ[key] if key in os.environ else None


def conf_loader(key, default):
    '''
    配置加载器， 优先从环境变量中加载， 如果没有从配置文件中加载
    仅接受字符串类型
    '''
    return env_loader(key) or file_loader(key) or default


def parse_args(key, default, parse_type=str):
    '''
    配置
    '''
    parse_result = conf_loader(key, default)
    if parse_type == int:
        return int(parse_result)
    if parse_type == bool:
        return True if str(parse_result).upper() == "TRUE" else False
    return str(parse_result)
