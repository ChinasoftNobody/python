from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer

from p2pshare import Node, OK, FAIL


class PeerNode(Node):
    port = None
    target_host = None
    server: SimpleXMLRPCServer = None

    def list_files(self, sub_path=''):
        super().list_files(sub_path)

    def register(self, node):
        super().register(node)

    def configure(self, port, target):
        self.port = port
        self.target_host = target

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
