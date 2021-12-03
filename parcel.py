from enum import IntEnum

class Mode(IntEnum):
    CONVERSE = 1
    WHISPER = 2
    SERVER_COMMAND = 3
    QUIT = 4

class ServerCommands(IntEnum):
    STOP = 1
    RESTART = 2
    
class Lingo(IntEnum):
    PICKLE = 1
    JSON = 2
    
class Parcel(object):

    lingo = Lingo.PICKLE
    mode = Mode.CONVERSE
    msg = ''
    user = ''
    room = 'main'

    def __init__(self, lingo = None):
        if lingo != None:
            self.lingo = lingo
    
    def __str__(self):
        return (
            'mode: '+str(self.mode)
            +'; msg: '+self.msg
            +'; user: '+self.user
            +'; room: '+self.room
        )
  
    def pack(self):

        data = None
        if self.lingo == Lingo.PICKLE:
            import pickle
            data = pickle.dumps(self.parcel())

        elif self.lingo == Lingo.JSON:
            import json
            data = json.dumps(self.parcel())
       
        return data

    def parcel(self):
        return  {
            'mode': int(self.mode),
            'msg': self.msg,
            'user': self.user,
            'room': self.room,
        }
    
    def unpack(self, data):

        obj = {}
        
        if self.lingo == Lingo.PICKLE:
            import pickle
            obj = pickle.loads(data)

        elif self.lingo == Lingo.JSON:
            import json
            obj = json.loads(data)

        self.unparcel(obj)

    def unparcel(self, parcel):
        self.mode = parcel['mode']
        self.msg = parcel['msg']
        self.user = parcel['user']
        self.room = parcel['room']
