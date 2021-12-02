from meow import Meow
from yesno import YesNo

class GetUserDetails(Meow):

    def __init__(self):
        self.identify()
        self.getConnection()
        
    def getConnection(self):
        self.getServer()
        self.getPort()

    def getServer(self):
        server = ''
        while not self.isValidServer(server):
            server = input("What server do you want to connect to (default: "+self.constants.DEFAULT_SERVER+")?\n")
            if server.strip() == '':
                server = self.constants.DEFAULT_SERVER
                print('Defaulted to ' + server)
        print('')
        self.settings.server = server

    def isValidServer(self, server):
        return server.strip() != ''
    
    def getPort(self):
        port = ''
        
        while not self.isValidPort(port):
            port = input("What port is the server at (default: "+str(self.constants.DEFAULT_PORT)+")?\n")
            if port.strip() == '':
                port = str(self.constants.DEFAULT_PORT)
                print('Defaulted to '+port)
        print('')
        self.settings.port = int(port)
        
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
        self.settings.name = name
            
    def isValidName(self, name):
        return name.strip() != ''

class ConfirmAnswers(Meow):

    def __init__(self):
        self.getConfirmation()
        
    def getConfirmation(self):
        yn = YesNo()
        answer = ''

        while not yn.isYesOrNo(answer):
            answer = yn.ask(
                "You are "
                    + self.settings.name
                +" and you want to connect to "
                    + self.settings.server + ":" + str(self.settings.port)
                +". \n\nCorrect? "
            )

            if yn.isYes(answer):
                self.settings.confirmed = True
                break
            elif yn.isNo(answer):
                print('\n---\nOk, then try again (or hit C-c to quit)\n')
            else:
                print('\n--\n')
