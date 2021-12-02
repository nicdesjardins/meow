from sockets import AF_INET, socket, SOCK_STREAM
from threading import Thread
from parcel import Parcel, Mode, Lingo
'''
Listen for clients
Receive messages from clients
Dispatch messages to clients
Do things on the server (e.g. take commands)
Keep track of who's online
Allow folks to login/logout
'''

class Server(object):

    host = ''
    port = None

    server = socket(AF_INET, SOCK_STREAM)

    running = False
    
    clients = {}
    addresses = {}

    BUFFSIZE = 1024
    
    def __init__(self, port = 12345, server = ''):
        pass

    def start(self):
        if self.running:
            return

    def acceptIncomingConnections(self):
        while True:
            client, client_address = self.server.accept()
            self.addresses[client] = client_address
            Thread(target=self.handleClient, args=(client,)).start()

    def handleClient(self, client):
        while True:
            data = client.recv(self.BUFFSIZE)
        
