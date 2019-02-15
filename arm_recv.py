
from Node import Node

node = Node("arm_recv_node.json")

while True:
    print("ARM: " + node.recv_simple("arm-controls"), flush=True, end="\r")
