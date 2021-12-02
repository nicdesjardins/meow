from meow import Meow
from config import GetUserDetails, ConfirmAnswers

class MeowClient(Meow):

    def start(self):
        try:
            while not self.settings.confirmed:
                GetUserDetails()
                ConfirmAnswers()
            
            print("\nOK, then we're all set to keep going!\n")

        except KeyboardInterrupt as ex:
            print('\nOk then, bye!')
            pass

class ConnectToServer(Meow):
    def __init__(self):
        pass
    
if __name__ == '__main__':
    mc = MeowClient()
    mc.start()
