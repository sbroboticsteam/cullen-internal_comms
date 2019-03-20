import json
import time
import numpy as np
from Node import Node

node = Node("test_node.json")


while True:    

    data = np.array([1, 2, 3, 4])
    node.send_nparray("inputs", data, copy=False)
    print("Message Sent: ")
    print(data)

    data = node.recv_nparray("inputs")
    time.sleep(1)
    print("Message Received: ")
    print(data)
    time.sleep(1)
