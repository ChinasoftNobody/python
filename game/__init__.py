import datetime
import logging.config
import os
import tkinter as tk

MENU_SIZE = 800, 600
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)  # 创建路径
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },

        "default": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": os.path.join(LOG_DIR, LOG_FILE),
            'mode': 'w+',
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 20,
            "encoding": "utf8"
        },
    },

    "loggers": {
        "app_name": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        'handlers': ['default'],
        'level': "INFO",
        'propagate': False
    }
}
logging.config.dictConfig(LOGGING)


class MenuMeta:
    def get_game_names(self) -> list:
        """
        获取游戏名称信息
        :return: 名称信息
        """
        pass

    def run_game(self, game_name) -> None:
        """
        启动游戏
        :param game_name: 游戏名称
        :return: None
        """
        pass

    def stop_games(self) -> None:
        """
        结束所有游戏
        :return: None
        """
        pass

    def init_menu(self) -> None:
        """
        初始化游戏菜单
        :return: None
        """
        pass

    def exit_game(self) -> None:
        """
        退出游戏
        :return:None
        """
        pass
