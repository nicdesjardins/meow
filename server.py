from socket import AF_INET, socket, SOCK_STREAM
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

    client_limit = 5
    
    clients = {}
    addresses = {}
    
    BUFFSIZE = 1024
    
    def __init__(self, port = 1234, host = ''):
        self.host = host
        self.port = port

    def stop(self):
        if self.running:
            print("Stopping...")
        else:
            print("Not running...")
        
    def start(self):
        if not self.running:
            print("Starting...")
            self.server.bind((self.host, self.port))
            self.server.listen(self.client_limit)
            self.accept_thread = Thread(target=self.acceptIncomingConnections)
            self.accept_thread.start()
            self.running = True
            print("Listening for a max of "+str(self.client_limit)+" connections @ "+self.host+":"+str(self.port))
        else:
            print("Already running...")

    def acceptIncomingConnections(self):
        while True:
            client, client_address = self.server.accept()
            self.addresses[client] = client_address
            Thread(target=self.handleClient, args=(client,)).start()

    def handleClient(self, client):
        print("Client "+str(client.fileno())+" connected from "+str(self.addresses[client]))
        p = Parcel()
        p.msg = 'Hello, World!'
        data = p.pack()
        client.sendall(data)
        
        while True:
            data = client.recv(self.BUFFSIZE)
            self.handleClientData(data)

    def handleClientData(self, data):
        p = Parcel()
        p.unpack(data)
        print("Received data from client: "+str(p))
        
if __name__ == '__main__':
    s = Server()
    s.start()
