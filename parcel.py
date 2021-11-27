import pickle

class Mode(Enum):
    CONVERSE = 1
    WHISPER = 2
    SERVER_COMMAND = 3
    QUIT = 4

class Lingo(Enum):
    PICKLE = 1
    JSON = 2
    
class Parcel(object):

    lingo = Lingo.PICKLE
    mode = Mode.CHAT
    msg = ''
    user = ''
    room = 'main'

    def __init__(self, lingo = None):
        if lingo != None:
            self.lingo = lingo
    
    def __str__(self):
        return (
            'mode: 'str(self.mode)
            +'; msg: '+self.msg
            +'; user: '+self.user
            +'; room: '+self.room
        )
  
    def pack(self):

        def pickle():
            import pickle
            return pickle.dumps(self.parcel())

        def json():
            import json
            return json.dumps(self.parcel())

        switch={
            Lingo.PICKLE: pickle(),
            Lingo.JSON: json(),
        }
        
        return switch.get(self.lingo)

    def parcel(self):
        return  {
            'mode': self.mode,
            'msg': self.msg,
            'user': self.user,
            'room': self.room,
        }
    
    def unpack(self, data):
        
        def pickle():
            import pickle
            return pickle.loads(data)

        def json():
            import json
            return json.loads(data)

        switch={
            Lingo.PICKLE: pickle(),
            Lingo.JSON: json(),
        }
        
        self.unparcel(switch.get(self.lingo))

    def unparcel(self, parcel):
        self.mode = parcel['mode']
        self.msg = parcel['msg']
        self.user = parcel['user']
        self.room = parcel['room']
