import json
import zmq
import traceback


class Node():
    """This is the class that will be the base of every node object

    Each node will read a config file in JSON format to initialize zmq sockets.
    The sockets will be stored in a dict with the key being the topic and the value being the socket
    To create a node, make a config file and extend the run() method.
    Further functionality is on the way.
    """

    def __init__(self, configPath):
        f = open(configPath)
        self.configPath = configPath
        self.configData = json.load(f)
        f.close()
        self.id = self.configData['id']
        self.context = zmq.Context()
        self.topics = {}
        self.initzmq()

    def stopzmq(self):
        """ Shuts down all zmq stuff


        """

        self.context.destroy()

    def loop(self):
        """ The main node code that gets executed every loop

        This is the method that should be overridden for the node to do stuff
        So help me God if anyone overrides this and puts a while true in there
        """

        print(self.id + " needs an overridden loop method")

    # TODO: use new helper methods
    def initzmq(self):
        """This method initializes zmq sockets and places them in the topics dict

        It will throw exceptions if the JSON it was fed is not correct
        """

        if "model" not in self.configData:
            raise Exception("model not found in %s" % self.configPath)

        if "topics" not in self.configData:
            raise Exception("Topics or port not found in %s" % self.configPath)

        for topic in self.configData['topics']:
            for x, y in topic.items():
                if y == "pub" or y == "rep":
                    if y == "pub":
                        socket = self.context.socket(zmq.PUB)
                    else:
                        socket = self.context.socket(zmq.REP)
                    socket.bind(
                        self.configData['protocol'] + "://*:%s" % self.configData['port'])
                    self.topics[x] = socket
                elif y == "sub" or y == "req":
                    if y == "sub":
                        socket = self.context.socket(zmq.SUB)
                    else:
                        socket = self.context.socket(zmq.REQ)
                    print(self.configData['protocol'] +
                          "://localhost:%s" % self.configData['port'])
                    socket.connect(
                        self.configData['protocol'] + "://localhost:%s" % self.configData['port'])
                    if y == "sub":
                        socket.setsockopt_string(zmq.SUBSCRIBE, x)
                    self.topics[x] = socket
                else:
                    raise Exception("Topic %s should be either pub or sub" % x)

    def gen_address(self, protocol, address, port):
        """ This method builds a url from info in a json file

        It can create a url for ipc, udp and tcp.
        It will throw exceptions if the protocol is invalid
        """

        url = ""

        if protocol == "tcp":
            url = "tcp://"
        elif protocol == "udp":
            url = "udp://"
        elif protocol == "ipc":
            url = "ipc://"
        else:
            raise Exception("Protocol not ipc or udp or tcp")

        url += address

        if protocol == "tcp" or protocol == "udp":
            url += ":" + port

        return url

    def build_socket(self, paradigm, topic, url):
        """ This method creates a socket from a paradigm and a url


        """

        socket = None
        if paradigm == "sub":
            socket = self.context.socket(zmq.SUB)
            socket.connect(url)
            socket.setsockopt_string(zmq.SUBSCRIBE, topic)
        elif paradigm == "pub":
            socket = self.context.socket(zmq.PUB)
            socket.connect(url)
        elif paradigm == "req":
            socket = self.context.socket(zmq.REQ)
            socket.bind(url)
        elif paradigm == "rep":
            socket == self.context.socket(zmq.REP)
            socket.bind(url)
        else:
            raise Exception("Please provide a valid paradigm")

        return socket

    def send(self, topic, msg):
        """This method can be used to send messages for the pub pattern

        The first argument is the topic to send the message on and the second
        is the message body
        """
        self.topics[topic].send_string("%s %s" % (topic, msg))

    # TODO: implement a timeout
    def recv(self, topic, callback):
        """This method is used to receive messages for the sub pattern

        The first argument is the topic to look for messages on.
        The second argument is a function to be executed with the message
        received being passed to it as an argument
        NOT VERIFIED: This method is blocking, and will interrupt execution
        until a message is received
        """
        re = self.topics[topic].recv_string()
        callback(re)

    def request(self, topic, req, callback):
        """This method is used to send a request to a node

        The first argument is the topic(in this case, the node) to send a
        request to.
        The second argument is the request to send
        The third argument is a callback function to process the reply from
        the server. The reply will be a string
        """
        self.topics[topic].send_string(req)
        msg = self.topics[topic].recv_string()
        callback(msg)

    def reply(self, topic, callback):
        """This method is used to send a reply to a node

        The first argument is the topic(in this case, the node) to reply to
        The second argument is a callback that will handle the request sent to
        this node. It must return a string.
        The reply generated by the callback is sent as a reply to the node
        that sent a request
        """
        msg = self.topics[topic].recv_string()
        rep = callback(msg)
        self.topics[topic].send_string(str(rep))
