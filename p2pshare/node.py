import logging
import os
from threading import Thread
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

from p2pshare import Node, OK, FAIL

SUCCESS = 'success'
LOG = logging.getLogger(__file__)


class PeerNode(Node):
    port: int = None
    target_host: str = None
    path: str = None
    target_node: Node = None
    server: SimpleXMLRPCServer = None
    __target_hosts: list = list()

    def list_files(self, sub_path='') -> tuple:
        if not sub_path:
            sub_path = self.path
        file_list = os.listdir(sub_path)
        file_info_list: list > FileInfo = list()
        for file in file_list:
            if os.path.isfile(os.path.join(sub_path, file)):
                file_info_list.append(
                    FileInfo(file, os.path.join(sub_path, file), 'file', os.path.getsize(os.path.join(sub_path, file)), os.path.getmtime(os.path.join(sub_path, file))))
            elif os.path.isdir(os.path.join(sub_path, file)):
                file_info_list.append(
                    FileInfo(file, os.path.join(sub_path, file), 'dir', os.path.getsize(os.path.join(sub_path, file)), os.path.getmtime(os.path.join(sub_path, file))))
            else:
                pass
        return OK, file_info_list

    def register(self, node) -> tuple:
        if node not in self.__target_hosts:
            self.__target_hosts.append(node)
        return OK, SUCCESS

    def configure(self, port=None, target=None, path=None) -> tuple:
        if port:
            self.port = port
        if target:
            self.target_host = target
        if path:
            self.path = path
        return OK, SUCCESS

    def connect_to_target(self) -> tuple:
        self.target_node: PeerNode = ServerProxy(self.target_host, allow_none=True)
        status, message = self.target_node.register(self)
        if status == OK:
            LOG.info(message)
            status, list_files = self.target_node.list_files()
            if status == OK:
                return OK, list_files
            else:
                return FAIL, 'get remote file list error'
        else:
            return FAIL, 'connect to target node failed'

    def start_server(self) -> tuple:
        try:
            def run():
                self.server = SimpleXMLRPCServer(("", self.port))
                self.server.register_instance(self)
                self.server.serve_forever()

            thread = Thread(target=run)
            thread.start()
            return OK, ('server started on port : %s' % self.port)
        except Exception as e:
            return FAIL, e

    def stop_server(self) -> tuple:
        if self.server:
            self.server.server_close()
        return OK, 'server stop'


class FileInfo:
    _name: str = None
    _path: str = None
    _type: str = None
    _size: int = None
    _m_time: str = None

    def __init__(self, name: str, path: str, type: str, size: int, m_time: str) -> None:
        super().__init__()
        self._name = name
        self._path = path
        self._type = type
        self._size = size
        self._m_time = m_time

    def get_name(self) -> str:
        return self._name

    def get_path(self) -> str:
        return self._path

    def get_type(self) -> str:
        return self._type

    def get_size(self) -> int:
        return self._size

    def get_m_time(self) -> str:
        return self._m_time
