"""
节点管理
"""

from node import Node


class NodeManager:
    node_list = {}

    def add(self, node: Node):
        """
        更新节点
        :param node:
        :return:
        """
        self.node_list.update({node.node_name: node})


nodeManager = NodeManager()