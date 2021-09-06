"""
流言算法进行初始节点发现
"""
from ant.core.zendiscovery.node import Node
from node_manager import nodeManager
from typing import List

class Gossip:

    def __init__(self, init_list: List[Node]):
        for item in init_list:
            nodeManager.add(item)


    def send_gossip(self):
        """
        发送流言
        :return:
        """
        #todo: 发送流言


    def get_gossip(self, gossip_resp: str):
        """
        收到流言
        :param gossip_resp:
        :return:
        """
