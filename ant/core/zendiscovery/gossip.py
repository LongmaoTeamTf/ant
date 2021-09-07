"""
流言算法进行初始节点发现
"""
import json

import requests
import rx
from rx import operators

from ant.core.zendiscovery.node import Node
from node_manager import nodeManager
from typing import List, Optional


class Gossip:

    def __init__(self, init_list: List[Node]):
        for item in init_list:
            nodeManager.add(item)

    def send_one_gossip(self):
        """
        发送流言
        :return:
        """
        source = rx.of(nodeManager.node_list)
        result_list = source.pipe(
            operators.map(lambda node: self.send_one_node(node)),
            operators.filter(lambda data: data is not None),
            operators.to_list()
        ).run()

        nodeManager.add_all(result_list)

    @staticmethod
    def send_one_node(node: Node) -> Optional[Node]:
        result_response = requests.post("%s:%s%s" % (node.node_name, node.port, "/node/gossip"), json={
            'node_list': json.dumps(item.__dict__ for item in nodeManager.node_list)
        }, timeout=0.2)
        if result_response.status_code == 200:
            return Node(**result_response.json())
        else:
            return None

    def send_gossip(self):
        """
        发送三轮流言
        :return:
        """
        source = rx.timer(0, 3, None)
        source.pipe(
            operators.take(3),
            operators.do_action(lambda _: self.send_one_gossip()),
        ).run()
