
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
from threading import Thread

class UI(object):

    INPUT_HEIGHT = 3
    
    def __init__(self, userInputHandler = None):
        self.userInputHandler = userInputHandler

    def start(self):
        curses.wrapper(self.run)
        
    def run(self, window):
        self.window = window
        
        self.width, self.height = self.getDimensions()
        self.screen = curses.initscr()
        
        self.outputWin = curses.newwin(
            self.height - self.INPUT_HEIGHT
            , self.width
            , 0
            , 0
        )
        self.outputWin.refresh()
        self.outY = 0
        self.outX = 0
        
        self.inputWin = curses.newwin(
            self.INPUT_HEIGHT
            , self.width
            , self.height - self.INPUT_HEIGHT
            , 0
        )
        
        #self.screen.move(self.height - self.INPUT_HEIGHT, 0)
        #self.inputWin.refresh()
        #self.screen.refresh()
        self.resetInput()

        self.input_thread = Thread(target=self.inputThread)
        self.input_thread.start()
        

    def inputThread(self):
        while True:
            try:
                ch = self.screen.getch()
                self.inputWin.addch(self.inY, self.inX, ch)
                self.inX += 1
                self.inXScr = self.inX
                self.screen.move(self.inYScr, self.inX)
                self.input_str += chr(ch)

                if self.hitEnterKey(ch):
                    if self.userInputHandler != None:
                        self.userInputHandler(self.input_str.strip())
                    self.resetInput()
                
                self.screen.move(self.inYScr, self.inXScr)
                #self.inputWin.refresh()
                self.screen.refresh()
                
            except Exception as ex:
                pass
    
    def resetInput(self):
        self.inputWin.erase()
        self.inX = 0
        self.inY = 0
        self.inYScr = self.height - self.INPUT_HEIGHT
        self.inXScr = 0
        self.input_str = ''
        self.screen.move(self.inYScr, self.inXScr)
        self.screen.refresh()
        self.inputWin.refresh()
        
    def addStringToOutput(self, string):
        self.outputWin.addstr(self.outY, 0, string)
        self.outY += 2
        self.outputWin.refresh()
        self.screen.refresh()
        
    def hitEnterKey(self, ch = None):
        if ch == None:
            ch = self.ch
        return self.isNewline(ch)
    
    def isNewline(self, ch):
        return ch in { curses.KEY_ENTER, 10, 13}
    
    def getDimensions(self):
        size = os.get_terminal_size()
        return [size.columns-1, size.lines-1]

if __name__ == '__main__':
    ui = UI()
    curses.wrapper(ui.run)

