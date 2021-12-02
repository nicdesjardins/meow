from meow import Meow
from config import GetUserDetails, ConfirmAnswers
from network_client import NetworkClient
from parcel import Parcel

'''
MeowClient:
- Inherits Meow
- Gets config from config.py (config.py inherits from Meow)

To do:
- Connect to a server w/ network_client (will it inherit Meow?)
- Convert its object(s) into data using Parcel
- Send data converted by Parcel to the server via the network_client
- network client will receive data
- data will be converted back to a usable object by Parcel
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

        except KeyboardInterrupt as ex:
            print('\nOk then, bye!')
            pass
    
    def netHandler(self, data):
        p = Parcel()
        p.unpack(data)
        print("Received " +str(p))

class ConnectToServer(Meow):
    def __init__(self):
        pass
    
if __name__ == '__main__':
    mc = MeowClient()
    mc.start()
