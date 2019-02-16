
from Node import Node

node = Node("controls_recv_test.json")

while True:
    print(node.recv_simple("drive"))
    print(node.recv_simple("arm"))
