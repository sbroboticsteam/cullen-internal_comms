
from Node import Node

node = Node("arm_recv_test.json")

while True:
    print("ARM: " + node.recv_simple("arm-controls"), flush=True, end="\r")
