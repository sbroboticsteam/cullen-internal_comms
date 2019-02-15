
from Node import Node

node = Node("drive_recv_test.json")

while True:
    print("DRIVE: " + node.recv_simple("drive"), end="\r", flush=True)
