from meow import Meow
from config import GetUserDetails, ConfirmAnswers
from network_client import NetworkClient
from parcel import Parcel

'''
MeowClient:
- Inherits Meow
- Gets config from config.py (config.py inherits from Meow)

To do:
- MeowClient will then action (e.g. display w/ ui, do an action, etc)
'''

class MeowClient(Meow):

    def start(self):
        try:
            while not self.settings.confirmed:
                GetUserDetails()
                ConfirmAnswers()
            
            print("\nOK, then we're all set to keep going!\n")
            self.netClient = NetworkClient(self.settings.server, self.settings.port, self.netHandler)
            self.netClient.connect()
            self.sendHelloToServer()

        except KeyboardInterrupt as ex:
            print('\nOk then, bye!')
            pass
        
    def sendHelloToServer(self):
        p = Parcel()
        p.msg = 'Hello from '+self.settings.name+"!"
        self.netClient.send(p.pack())
            
    def netHandler(self, data):
        p = Parcel()
        p.unpack(data)
        print("Received: " +str(p))

class ConnectToServer(Meow):
    def __init__(self):
        pass
    
if __name__ == '__main__':
    mc = MeowClient()
    mc.start()
