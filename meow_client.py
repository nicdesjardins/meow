from meow import Meow
from config import GetUserDetails, ConfirmAnswers
from network_client import NetworkClient
from parcel import Parcel
from ui import UI
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
            
            self.netClient = NetworkClient(self.settings.server, self.settings.port, self.netHandler)
            self.netClient.connect()
            self.ui = UI(self.userInputHandler)
            self.ui.start()

        except KeyboardInterrupt as ex:
            print('\nOk then, bye!')
            pass

    def userInputHandler(self, string):
        p = Parcel()
        p.msg = string
        self.netClient.send(p.pack())
            
    def netHandler(self, data):
        p = Parcel()
        p.unpack(data)
        self.ui.addStringToOutput(p.msg)

class ConnectToServer(Meow):
    def __init__(self):
        pass
    
if __name__ == '__main__':
    mc = MeowClient()
    mc.start()
