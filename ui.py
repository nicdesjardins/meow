
'''
UI Does:

- starts/handles curses, including:
-- input area
-- output area
-- buffer list (rooms, private chats, etc)

- handles keyboard (and mouse) input
- displays from:
-- user
-- other users
-- feedback from the app

'''

import curses
import os

class UI(object):

    def __init__(self):
        pass

    def start(self, window):

        self.window = window
        
        self.width, self.height = self.getDimensions()
        self.screen = curses.initstr()
        
        self.outputWin = curses.newwin(self.height - 5, self.width, 0, 0)
        self.inputWin = curses.newwin(self.5, self.width, self.height - 5, 0)

    def getDimensions(self):
        size = os.get_terminal_size()
        return [size.columns-1, size.lines-1]

def main(window = None):


if __name__ == '__main__':
    ui = UI()
    curses.wrapper(ui.start)
