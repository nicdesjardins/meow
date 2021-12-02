

class Config(object):
    name = ''
    server = ''
    port = None
    confirmed = False

class Constants(object):
    DEFAULT_SERVER = '127.0.0.1'
    DEFAULT_PORT = 1234

class Meow(object):
    constants = Constants()
    settings = Config()
