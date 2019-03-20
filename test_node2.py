import json
import time
import numpy as np
from Node import Node

node = Node("test_node2.json")


while True:    

    data = node.recv_nparray("inputs")
    time.sleep(1)
    print("Message Received: ")
    print(data)
    time.sleep(1)

    data = np.array([4, 3, 2, 1])
    node.send_nparray("inputs", data, copy=False)
    print("Message Sent: ")
    print(data)
