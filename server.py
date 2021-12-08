from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from parcel import Parcel, Mode, Lingo
import errno
'''
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
    DEFAULT_PORT = 1234
    
    def __init__(self, port = None, host = ''):
        self.host = host
        if port != None:
            self.port = port
        else:
            self.port = self.DEFAULT_PORT

    def stop(self):
        if self.running:
            print("Stopping...")
        else:
            print("Not running...")
        
    def start(self):
        if not self.running:
            print("Start listening on port "+str(self.port))
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
        self.clients[client] = client.fileno()
        
        while True:
            data = client.recv(self.BUFFSIZE)
            self.handleClientData(data, client)

    def handleClientData(self, data, client):
        p = Parcel()
        p.unpack(data)
        
        print("Received data from client ["+str(client.fileno())+"]: "+str(p))
        self.broadcast(data, client)
        
    def broadcast(self, data, client):
        for sock in self.clients:
            try:
                sock.sendall(data)
            except Exception as ex:
                if ex.errno ==  errno.EPIPE:
                    client.close()
                    del clients[client]
                    print("caught broken pipe!")
                print("Caught exception when trying to send to client "+str(sock.fileno())+".Ex:\n"+str(ex)+"\nerrno:"+str(ex.errno))
        
if __name__ == '__main__':
    import sys
    port = None
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            print("Invalid port: "+str(sys.argv[1]))
            exit(0)
    
    s = Server(port)
    s.start()
