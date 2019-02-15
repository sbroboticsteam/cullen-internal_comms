
from Node import Node
import json
import time

node = Node("arm_send.json")

while True:
    data = json.loads('{}')
    data['id'] = input("id: ")
    data['angle'] = input("angle: ")
    msg = json.dumps(data)
    node.send("arm-controls", msg)
