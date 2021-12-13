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

class TesteurDeUI(Meow):

    def start(self):
        try:
            self.ui = UI(self.userInputHandler)
            self.ui.start()

        except KeyboardInterrupt as ex:
            print('\nOk then, bye!')
            pass

    def userInputHandler(self, string):
        self.ui.addStringToOutput(string)
            
class ConnectToServer(Meow):
    def __init__(self):
        pass
    
if __name__ == '__main__':
    tui = TesteurDeUI()
    tui.start()
