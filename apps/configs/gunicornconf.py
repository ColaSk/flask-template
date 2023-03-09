import multiprocessing
import os
from sys import stdout

from configs import base, sysconf

if not os.path.exists(sysconf.LOG_DIR):
    os.makedirs(sysconf.LOG_DIR)

bind = sysconf.BIND

# 启动的进程数
workers = sysconf.WORK_NUMS or multiprocessing.cpu_count()

x_forwarded_for_header = 'X-FORWARDED-FOR'

loglevel = sysconf.LOG_LEVEL

# timeout
timeout = 30

file_name = os.path.join(sysconf.LOG_DIR, "log.log")
simple_format = '[%(asctime)s: %(levelname)s/%(processName)s (%(filename)s:%(funcName)s:%(lineno)d)] %(message)s'

# 这里的logging会直接复写掉app的logger.
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {},
    'formatters': {
        'default': {
            'format': simple_format
        },
        'simple': {
            'format': simple_format
        }
    },
    'loggers': {
        "gunicorn.error": {
            "handlers": ["default_outfile", "stream"],  # 对应下面的键
            "qualname": "gunicorn.error",
            "level": loglevel,
        },
        "gunicorn.access": {
            "handlers": ["default_outfile", "stream"],
            "qualname": "gunicorn.access",
            "level": loglevel
        },
        base.PROJECT_NAME: {
            "handlers": ["default_outfile", "stream"],
            "level": loglevel
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'default_outfile': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': file_name,
            'when': 'midnight',
            'backupCount': 10,
            'encoding': 'utf-8',
        },
        "stream": {
            "class": "logging.StreamHandler",
            "stream": stdout
        }
    }
}

# 如果部署的时候开启了debug模式, 可以启用auto_reload
reload = sysconf.AUTO_RELOAD
