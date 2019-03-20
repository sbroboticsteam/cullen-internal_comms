import json
import time
import numpy as np
from Node import Node

node = Node("test_node2.json")


while True:    
    data = node.recv_nparray("inputs")
    print("Message Received: ")
    print(data)
    data = np.array([2, 3, 1, 0])
    node.send_nparray("inputs", data, copy=False)
    print("Message Sent: ")
    print(data)
