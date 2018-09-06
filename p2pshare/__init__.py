import datetime
import logging.config
import os
from threading import Thread
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

OK = 0
FAIL = -1
WINDOW_SIZE = 800, 600
APP_NAME = 'p2p share'
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
        'handlers': ['default', 'console'],
        'level': "INFO",
        'propagate': False
    }
}
logging.config.dictConfig(LOGGING)


class Node:

    def list_files(self, sub_path=''):
        """
        查询当前节点文件列表，包含目录及文件
        :return: 结果信息
        """
        pass

    def register(self, node):
        """
        新节点注册发现，node为非己方节点
        :param node: 非己方节点
        :return:注册结果
        """
        pass

    def configure(self, port, target):
        """
        匹配基本信息
        :param port: 本机端口
        :param target: 目标机器
        :return: 结果
        """
        pass


class P2PUtil:

    @staticmethod
    def start_peer(node):
        master_server = ServerProxy(node.host, allow_none=True)
        node.master_server = master_server
        master_server.registered(node)

        def _run():
            peer_node = SimpleXMLRPCServer(("", node.port))
            peer_node.register_instance(node)
            peer_node.serve_forever()
            pass

        thread = Thread(target=_run())
        thread.start()
        return OK


class P2PError(Exception):

    def __init__(self):
        Exception.__init__(self, 'err')
        # log = logging.getLogger(__file__)
        # log.error('error:')
