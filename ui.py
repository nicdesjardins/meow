
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
    WHITE_ON_BLUE = 1
    BLUE_ON_WHITE = 2
    
    def __init__(self, userInputHandler = None):
        self.userInputHandler = userInputHandler

    def start(self, userInputHandler = None):
        if userInputHandler != None:
            self.userInputHandler = userInputHandler
        
        curses.wrapper(self.run)

    def run(self, window):

        self.window = window
        self.width, self.height = self.getDimensions()

        curses.init_pair(self.WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(self.BLUE_ON_WHITE, curses.COLOR_BLUE, curses.COLOR_WHITE)
        
        self.screen = curses.initscr()
        self.screen.bkgd(' ', curses.color_pair(self.BLUE_ON_WHITE))
        
        self.outputWin = curses.newpad(self.height - self.INPUT_HEIGHT, self.width)
        self.outputWin.bkgd(' ', curses.color_pair(self.WHITE_ON_BLUE))
        self.outputWin.border()
        self.refreshOutputWin()
        
        self.inputWin = curses.newpad(self.INPUT_HEIGHT, self.width)
        self.refreshInputWin()
        
        self.inputWin.bkgd(' ', curses.color_pair(self.BLUE_ON_WHITE))
        self.inputWin.border()
        
        self.resetInput()
        
        self.input_thread = Thread(target=self.inputThread)
        self.input_thread.start()
        
    def refreshOutputWin(self):
        pminrow = 0
        pmincol = 0
        sminrow = 0
        smincol = 0
        smaxrow = self.height - self.INPUT_HEIGHT
        smaxcol = self.width
        self.outputWin.refresh(pminrow,pmincol, sminrow,smincol, smaxrow,smaxcol)
        
    def refreshInputWin(self):
        pminrow = 0
        pmincol = 0
        sminrow = self.height - self.INPUT_HEIGHT
        smincol = 0
        smaxrow = self.height
        smaxcol = self.width
        self.inputWin.refresh(pminrow,pmincol, sminrow,smincol, smaxrow,smaxcol)
        
    def inputThread(self):
        while True:
            try:
                ch = self.screen.getch()
                self.inX += 1
                self.inXScr = self.inX
                self.input_str += chr(ch)

                if self.hitEnterKey(ch):
                    if self.input_str.strip() != '':
                        if self.userInputHandler != None:
                            self.userInputHandler(self.input_str.strip())
                    self.resetInput()
                
            except Exception as ex:
                pass
    
    def resetInput(self):
        self.inX = 1
        self.inY = 1
        self.inYScr = (self.height - self.INPUT_HEIGHT) + 1
        self.inXScr = self.inX
        self.input_str = ''
        self.screen.move(self.inYScr, self.inXScr)
        self.screen.refresh()
        self.refreshInputWin()
        
    def addStringToOutput(self, string):
        self.outputWin.addstr(self.outY, self.outX, string)
        self.refreshOutputWin()
        self.outY += 2
        self.screen.move(self.inYScr, self.inXScr)
        self.screen.refresh()
        
    def hitEnterKey(self, ch = None):
        if ch == None:
            ch = self.ch
        return self.isNewline(ch)
    
    def isNewline(self, ch):
        return ch in { curses.KEY_ENTER, 10, 13}
    
    def getDimensions(self):
        size = os.get_terminal_size()
        return [size.columns, size.lines]

if __name__ == '__main__':
    ui = UI()
    curses.wrapper(ui.run)

