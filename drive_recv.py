
from Node import Node

node = Node("drive_recv_node.json")

while True:
    print("DRIVE: " + node.recv_simple("drive-controls"), end="\r", flush=True)
