import tkinter as tk
import logging
import time
from threading import Thread

from p2pshare import P2PError, DEFAULT_PORT, OK
from p2pshare.node import PeerNode

LOG = logging.getLogger(__file__)


class MainFrame(tk.Frame):
    message: str = None
    peer_node: PeerNode = None

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
        self.button_disconnect = tk.Button(text='停止监听', command=self.disconnect)
        self.button_disconnect.grid(row=0, column=5, sticky=tk.E)

        self.label_message_title = tk.Label(text='system info:')
        self.label_message_info = tk.Label(text='')
        self.label_message_title.grid(row=1, column=0, columnspan=5, sticky=tk.W)
        self.label_message_info.grid(row=2, column=0, columnspan=5, sticky=tk.W)

    def connect(self) -> None:
        """
        连接目标节点
        """
        port = DEFAULT_PORT
        target_host = ''
        try:
            port = int(self.entry_local_port.get())
            target_host = self.entry_target_node.get()
        except ValueError as e:
            self.message = e;
            self.label_message_info.config(text=self.message)
        LOG.info('local port:' + str(port))
        LOG.info('target node:' + target_host)
        self.peer_node.configure(port=port, target=target_host)
        status, message = self.peer_node.start_server()
        if status == OK:
            self.label_message_info.config(text=message)
            self.button_connect.configure(state='disabled')
        else:
            self.label_message_info.config(text=message)
            self.button_connect.configure(state='active')

    def disconnect(self) -> None:
        """
        停止服务
        :return:None
        """
        if self.peer_node:
            self.peer_node.stop_server()
        self.label_message_info.config(text='server stop')
        self.button_connect.configure(state='active')
