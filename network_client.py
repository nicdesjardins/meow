from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class NetworkClient(object):

    server = ''
    port = None
    
    socket = socket(AF_INET, SOCK_STREAM)
    connected = False
    
    receiveHandler = None
    receiveThread = None

    BUFFSIZE = 1024
    
    def __init__(self, server, port, receiveHandler):
        self.server = server
        self.port = port
        self.receiveHandler = receiveHandler
        self.receiveThread = Thread(target=self.receive)
        pass
    
    def connect(self, receiveHandler = None):
        # Create socket connection
        self.socket.connect((self.server, self.port))
        self.connected=True
        # Create a thread to handle incoming data, pass them to receiveHandler
        self.receiveThread.start()

    def disconnect(self):
        self.socket.close()
        self.connected = False
    
    def send(self, data):
        # Take our data send it via socket
        pass

    def receive(self):
        while self.connected:
            try:
                data = self.socket.recv(self.BUFFSIZE)
                self.receiveHandler(data)
