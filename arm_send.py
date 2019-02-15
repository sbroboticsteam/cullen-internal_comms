
from Node import Node
import json
import time

node = Node("arm_controls.json")

while True:
    data = json.loads('{}')
    data['id'] = input("id: ")
    data['angle'] = input("angle: ")
    msg = json.dumps(data).encode('utf-8')
    node.send("arm-controls", msg)
