import datetime
import tkinter as tk
from tkinter import ttk
import logging

from p2pshare import DEFAULT_PORT, OK, DEFAULT_TARGET, DEFAULT_PATH
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
        self.label_local_port = ttk.Label(text='本机端口:')
        self.label_local_port.grid(row=0, column=0, sticky=tk.E)
        self.entry_local_port = ttk.Entry()
        self.entry_local_port.insert(tk.END, DEFAULT_PORT)
        self.entry_local_port.grid(row=0, column=1, sticky=tk.E)
        self.label_local_path = ttk.Label(text='目录路径')
        self.label_local_path.grid(row=0, column=2, sticky=tk.E)
        self.entry_local_path = ttk.Entry()
        self.entry_local_path.insert(tk.END, DEFAULT_PATH)
        self.entry_local_path.grid(row=0, column=3, sticky=tk.E)
        self.button_start_server = ttk.Button(text='启动监听', command=self.start_server)
        self.button_start_server.grid(row=0, column=4, sticky=tk.E)
        self.button_disconnect = ttk.Button(text='停止监听', command=self.disconnect)
        self.button_disconnect.grid(row=0, column=5, sticky=tk.E)

        self.label_target_node = ttk.Label(text='目标地址:')
        self.label_target_node.grid(row=1, sticky=tk.E)
        self.entry_target_node = ttk.Entry()
        self.entry_target_node.insert(tk.END, DEFAULT_TARGET)
        self.entry_target_node.grid(row=1, column=1, sticky=tk.E)
        self.button_connect = ttk.Button(text='连接', command=self.connect)
        self.button_connect.grid(row=1, column=2, sticky=tk.E)

        self.label_message_title = ttk.Label(text='system info:')
        self.label_message_info = ttk.Label(text='')
        self.label_message_title.grid(row=2, column=0, columnspan=10, sticky=tk.W)
        self.label_message_info.grid(row=3, column=0, columnspan=10, sticky=tk.W)
        # 以下为文件列表模块
        columns = '名称', '修改日期', '大小', '类型'
        # 显示列
        self.tree_view_target_file_list = ttk.Treeview(self.master, height=20, show="headings", columns=columns)
        self.scrollbar_file_list = ttk.Scrollbar(self.master, orient="vertical",
                                                 command=self.tree_view_target_file_list.yview())
        self.tree_view_target_file_list.configure(yscroll=self.scrollbar_file_list.set)
        self.tree_view_target_file_list["columns"] = columns
        for i in range(len(columns)):
            if 0 < i < len(columns) - 1:
                self.tree_view_target_file_list.column(columns[i], anchor='e')
            else:
                self.tree_view_target_file_list.column(columns[i], anchor='w')
            self.tree_view_target_file_list.heading(columns[i], text=columns[i])

        self.tree_view_target_file_list.grid(row=4, columnspan=8, sticky=tk.W)
        self.scrollbar_file_list.grid(row=4, column=9, sticky="ns")

    def start_server(self) -> None:
        port = DEFAULT_PORT
        path = ''
        try:
            port = int(self.entry_local_port.get())
            path = self.entry_local_path.get()
        except ValueError as e:
            self.message = e
            self.label_message_info.config(text=self.message)
        self.peer_node.configure(port=port, path=path)
        status, message = self.peer_node.start_server()
        if status == OK:
            self.label_message_info.config(text=message)
            self.button_start_server.configure(state='disabled')
        else:
            self.label_message_info.config(text=message)
            self.button_start_server.configure(state='active')

    def connect(self) -> None:
        """
        连接目标节点
        """
        target_host = ''
        try:
            target_host = self.entry_target_node.get()
        except ValueError as e:
            self.message = e
            self.label_message_info.config(text=self.message)
        LOG.info('target host:' + target_host)
        self.peer_node.configure(target=target_host)
        if target_host:
            status, file_list = self.peer_node.connect_to_target()
            if status == OK:
                for child in self.tree_view_target_file_list.get_children():
                    self.tree_view_target_file_list.delete(child)
                for i in range(len(file_list)):
                    self.tree_view_target_file_list.insert("", i, text=file_list[i]['_name'],
                                                           values=(file_list[i]['_name'],
                                                                   datetime.datetime.fromtimestamp(
                                                                       file_list[i]['_m_time']).strftime(
                                                                       '%Y-%m-%d %H:%M:%S'),
                                                                   str(file_list[i]['_size']), file_list[i]['_type']))
            else:
                LOG.error('connect to target failed')
                self.label_message_info.config(text='connect to target failed')

    def disconnect(self) -> None:
        """
        停止服务
        :return:None
        """
        if self.peer_node:
            self.peer_node.stop_server()
        self.label_message_info.config(text='server stop')
        self.button_start_server.configure(state='active')
