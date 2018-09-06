from p2pshare import Node


class PeerNode(Node):
    port = None
    target_host = None

    def list_files(self, sub_path=''):
        super().list_files(sub_path)

    def register(self, node):
        super().register(node)

    def configure(self, port, target):
        self.port = port
        self.target_host = target
