import os

from utils.loader import conf_loader, parse_args

CURR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(CURR_PATH)
PROJECT_PATH = os.path.dirname(BASE)

STATIC_URL_PATH = '/statics'
STATIC_FOLDER = os.path.join(BASE, 'templates/statics')

LOG_DIR = os.path.join(PROJECT_PATH, "logs", "")  # 日志文件夹路径

# ######################################### 服务IP配置 #####################################

API_SERVER = conf_loader("API_SERVER", "127.0.0.1:5000")

# ######################################## Gunicorn配置  ########################################
LOG_LEVEL = parse_args("LOG_LEVEL", "INFO")  # 影响Gunicorn和Flask的LOGGER
AUTO_RELOAD = parse_args("AUTO_RELOAD", False, bool)  # 设置此项可以让gunicorn检测文件变化并且重启
WORK_NUMS = parse_args("WORKERS_NUMS", 1, int)  # 如果设置为0则自动设置
BIND = conf_loader("BIND", "0.0.0.0:8000")

# ######################################## Flask-JWT配置  ########################################
SSO_LOGIGN = conf_loader('SSO_LOGIGN', True)  # 是否支持单点登录 True:支持，False:不支持
JWT_ACCESS_TOKEN_EXPIRES = conf_loader('JWT_ACCESS_TOKEN_EXPIRES', 60 * 60 * 24)
LOGIN_KEY = conf_loader('LOGIN_KEY', "lk_")

# ###################################### Flasksqlalchemy配置  ####################################
# 是否使用连接池
USE_DB_POOL = parse_args("USE_DB_POOL", True, bool)

# 连接池配置, 如果USE_DB_POOL为false不生效
SQLALCHEMY_ENGINE_OPTIONS = dict(
    pool_size=parse_args("DB_POOL_SIZE", 5, int),  # 链接池数量
    # max_overflow=100,  # 当连接池中链接已经用完了, 最多还允许建立多少额外的链接
    # pool_timeout=5,   # 指定池的连接超时, 秒为单位
    # 连接池回收时间, 过了n秒之后连接池会释放过期链接并创建新链接, 这个值要小于mysql的max_timeout, 否则会lost connection, 默认8小时
    pool_recycle=parse_args("DB_POOL_RECYCLE", 8 * 60, int),
)

MYSQL_USER = conf_loader('MYSQL_USER', 'root')
MYSQL_PASSWD = conf_loader('MYSQL_PASSWD', 'root')
MYSQL_HOST = conf_loader('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = conf_loader('MYSQL_PORT', 3306)
MYSQL_DATABASE = conf_loader('MYSQL_DATABASE', "test")
MYSQL_CHARSET = conf_loader("MYSQL_CHARSET", "utf8mb4")

# ######################################## REDIS配置  ########################################
REDIS_CONFIG = {
    "type": conf_loader('REDIS_TYPE', 'single'),   # single, sentinel, cluster
    "host": conf_loader('REDIS_HOST', '127.0.0.1'),
    "port": conf_loader('REDIS_PORT', 6379),
    "password": conf_loader('REDIS_PASSWORD', ''),
    "username": conf_loader('REDIS_USERNAME', ''),
    "db": conf_loader('REDIS_DB', '7'),
    "decode_responses": True,
}
