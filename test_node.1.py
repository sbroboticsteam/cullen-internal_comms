import json
from Node import Node

node = Node("test_node.1.json")


while True:    
    data = [1]
    data[0] = input()
    msg = json.dumps(data).encode('utf-8')
    node.send("inputs-out",msg)

def shutdown(self):
    print("node shutting down")

