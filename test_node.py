
from Node import Node

node = Node("test_node.json")

while True:
    print(node.recv_simple("inputs-out"))
