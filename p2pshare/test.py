from p2pshare import Node, P2PUtil

node = Node('http://192.168.0.103:4242', 4141, '123', 'e:\\')
P2PUtil.start_peer(node)
