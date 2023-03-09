import logging
import logging.config
import os

from flask import Flask

from configs.sysconf import LOG_LEVEL, LOG_DIR

simple_format = '[%(asctime)s: %(levelname)s/%(processName)s (%(filename)s:%(funcName)s:%(lineno)d)] %(message)s'


def get_logging_config(logs_path: str, level: str) -> dict:
    """获取logging配置
    """
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': simple_format
            }
        },
        'handlers': {
            'console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'default': {
                'level': level,
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'filename': os.path.join(logs_path, 'default_api.log'),
                'when': 'midnight',
                'backupCount': 10,
                'encoding': 'utf-8',
            }
        },

        'root': {
            'handlers': ['default', "console"],
            'level': level
        }
    }


def _create_root_logger():
    config = get_logging_config(LOG_DIR, LOG_LEVEL)
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.config.dictConfig(config)
    logger = logging.getLogger('root')
    return logger


logger = _create_root_logger()


def init_logger(app: Flask, config: dict = None):
    """初始化 logger"""
    global logger

    if config:
        logging.config.dictConfig(config)
    app.logger = logger
