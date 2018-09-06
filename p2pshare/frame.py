import tkinter as tk
import logging
import time
from threading import Thread

from p2pshare import P2PError
from p2pshare.node import PeerNode

LOG = logging.getLogger(__file__)


class MainFrame(tk.Frame):

    def __init__(self, root=None):
        super().__init__(master=root)
        self._init_widgets()
        self.peer_node = PeerNode()

    def _init_widgets(self) -> None:
        """
        页面布局为网格布局
        """
        self.label_target_node = tk.Label(text='目标地址:')
        self.label_target_node.grid(row=0, sticky=tk.W)
        self.entry_target_node = tk.Entry()
        self.entry_target_node.grid(row=0, column=1, sticky=tk.E)
        self.label_local_port = tk.Label(text='本机端口:')
        self.label_local_port.grid(row=0, column=2, sticky=tk.E)
        self.entry_local_port = tk.Entry()
        self.entry_local_port.grid(row=0, column=3, sticky=tk.E)
        self.button_connect = tk.Button(text='连接', command=self.connect)
        self.button_connect.grid(row=0, column=4, sticky=tk.E)

    def connect(self):
        port = int(self.entry_local_port.get())
        target_host = self.entry_target_node.get()
        LOG.info('local port:' + str(port))
        LOG.info('target node:' + target_host)
        self.peer_node.configure(port=port, target=target_host)
        self.button_connect.configure(state='disabled')
        time.sleep(2)
        self.button_connect.configure(state='active')
        pass
