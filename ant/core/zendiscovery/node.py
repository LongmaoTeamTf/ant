"""
节点
"""


class Node:
    node_name: str
    port: str
    can_data: bool
    can_master: bool
    is_master: bool

    def __init__(self, node_name: str, port: str, can_data: bool, can_master: bool, is_master: bool):
        self.node_name = node_name
        self.port = port
        self.can_data = can_data
        self.can_master = can_master
        self.is_master = is_master
