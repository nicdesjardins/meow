from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from parcel import Parcel

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
        self.socket.connect((self.server, self.port))
        self.connected=True
        self.receiveThread.start()

    def disconnect(self):
        self.socket.close()
        self.connected = False
    
    def send(self, data):
        self.socket.sendall(data)
        pass

    def receive(self):
        while self.connected:
            try:
                data = self.socket.recv(self.BUFFSIZE)
                self.receiveHandler(data)
            except Exception as ex:
                print(str(ex))
                print(full_stack())
                pass

def full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if exc is not None:  # i.e. an exception is present
        del stack[-1]       # remove call of full_stack, the printed exception
                            # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
         stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr
