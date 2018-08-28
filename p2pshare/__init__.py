import os
from os.path import join, isfile
from threading import Thread
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

OK = 0
FAIL = -1


class Node:
    """
    p2p的节点，拥有主节点的信息，并且拥有自己的目录地址以及端口及密码
    可以访问自己的文件信息
    可以调用主节点，查询网络中节点的信息
    可以读取网络节点中文件信息，并写入自己的目录地址
    """

    def __init__(self, host, port, token, dir_name):
        super().__init__()
        self.host = host
        self.port = port
        self.token = token
        self.dir_name = dir_name

    def list_files(self, sub_path=''):
        """
        查询当前节点文件列表，包含目录及文件
        :return: 结果信息
        """
        dirs = list()
        files = list()
        for file in os.listdir(join(self.dir_name, sub_path)):
            if isfile(file):
                files.append(file)
            else:
                dirs.append(file)
        return OK, dirs, files

    def registered(self, node):
        """
        node
        :param node:
        :return:
        """
        print('hello', repr(node), repr(self))
        return OK


class P2PUtil:

    @staticmethod
    def start_master(node):
        """
        启动master节点监听
        :type node: 1
        :return: 结果
        """

        def _run():
            master_server = SimpleXMLRPCServer(("", node.port))
            master_server.register_instance(node)
            master_server.serve_forever()
            pass

        thread = Thread(target=_run())
        thread.start()
        return OK

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


if __name__ == '__main__':
    master_node = Node('', 4242, '123', 'd:\\')
    P2PUtil.start_master(master_node)
