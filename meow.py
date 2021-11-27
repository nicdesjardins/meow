
class Meow(object):

    name = ''
    server = ''
    port = None
    
    DEFAULT_SERVER = '127.0.0.1'
    DEFAULT_PORT = 1234
    
    def start(self):
        try:
            Init()
            
            answer = input("You are "+self.name+" and you want to connect to "+self.server + ":" + str(self.port)+"? ")
        except:
            print('\n')
            pass

class Init(Meow):

    def __init__(self):
        self.identify()
        self.connect()
        
    def connect(self):
        self.getServer()
        self.getPort()

    def getServer(self):

        server = ''

        while not self.isValidServer(server):
            server = input("What server do you want to connect to (default: "+self.DEFAULT_SERVER+")?\n")
            if server.strip() == '':
                server = self.DEFAULT_SERVER
                print('Defaulted to ' + server)
        print('')
        self.server = server

    def isValidServer(self, server):
        return server.strip() != ''
    
    def getPort(self):
        port = ''
        
        while not self.isValidPort(port):
            port = input("What port is the server at (default: "+str(self.DEFAULT_PORT)+")?\n")
            if port.strip() == '':
                port = str(self.DEFAULT_PORT)
                print('Defaulted to '+port)
        print('')
        self.port = int(port)
        
    def isValidPort(self, port):
        try:
            int(port)
            return True
        except:
            return False
    
    def identify(self):
        name = ''
        while not self.isValidName(name):
            name = input("What's your name?\n")
        print('')
        self.name = name
            
    def isValidName(self, name):
        return name.strip() != ''
    
    
if __name__ == '__main__':
    m = Meow()
    m.start()
