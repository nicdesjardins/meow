
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

    WHITE_ON_BLUE = 1
    BLUE_ON_WHITE = 2
    
    def run(self, window):

        self.window = window        
        self.width, self.height = self.getDimensions()

        self.screen = curses.initscr()
        curses.init_pair(self.WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(self.BLUE_ON_WHITE, curses.COLOR_BLUE, curses.COLOR_WHITE)
        
        self.screen.bkgd(' ', curses.color_pair(self.BLUE_ON_WHITE))
        self.screen.border()
        
        self.outputWin = curses.newpad(self.height - self.INPUT_HEIGHT, self.width+1)
        self.outY = 1
        self.outX = 1
        
        self.outputWin.bkgd(' ', curses.color_pair(self.WHITE_ON_BLUE))
        self.outputWin.border()
        self.refreshOutputWin()
        
        
        '''self.inputWin = curses.newwin(
            self.INPUT_HEIGHT
            , self.width
            , self.height - self.INPUT_HEIGHT
            , 0
        )'''
        self.inputWin = curses.newpad(self.INPUT_HEIGHT, self.width + 1)
        self.refreshInputWin()
        '''
        window.refresh([pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol])¶

        Update the display immediately (sync actual screen with previous drawing/deleting methods).

        The 6 optional arguments can only be specified when the window is a pad created with newpad(). The additional parameters are needed to indicate what part of the pad and screen are involved:
        - pminrow and pmincol specify the upper left-hand corner of the rectangle to be displayed in the pad. 
        - sminrow, smincol, smaxrow, and smaxcol specify the edges of the rectangle to be displayed on the screen. 
        - The lower right-hand corner of the rectangle to be displayed in the pad is calculated from the screen coordinates, since the rectangles must be the same size. 
        - Both rectangles must be entirely contained within their respective structures. 
        - Negative values of pminrow, pmincol, sminrow, or smincol are treated as if they were zero.
        '''

        #self.inputWin.refresh( 0,0, 0,0, 
        
        self.inputWin.bkgd(' ', curses.color_pair(self.BLUE_ON_WHITE))
        self.inputWin.border()
        
        #self.inputWin.attron(curses.color_pair(1) | curses.A_REVERSE)
        self.resetInput()
        
        self.input_thread = Thread(target=self.inputThread)
        self.input_thread.start()
        
        #self.inputThread()
    def refreshOutputWin(self):
        pminrow = 0
        pmincol = 0
        sminrow = 0
        smincol = 0
        smaxrow = self.height - self.INPUT_HEIGHT
        smaxcol = self.width + 1
        self.outputWin.refresh( pminrow,pmincol, sminrow,smincol, smaxrow,smaxcol )
        
    def refreshInputWin(self):
        pminrow = self.height - self.INPUT_HEIGHT
        pmincol = 0
        sminrow = pminrow
        smincol = pmincol
        smaxrow = self.INPUT_HEIGHT
        smaxcol = self.width
        #try:
        self.inputWin.refresh( pminrow,pmincol, sminrow,smincol, smaxrow,smaxcol )
        #except Exception as ex:
        #    print(ex)
        
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
        self.inputWin.erase()
        self.inX = 1
        self.inY = 1
        self.inYScr = (self.height - self.INPUT_HEIGHT) + 1
        self.inXScr = self.inX
        self.input_str = ''
        self.screen.move(self.inYScr, self.inXScr)
        self.screen.refresh()
        self.refreshInputWin()
#        self.inputWin.refresh()
        
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
        return [size.columns-1, size.lines-1]

if __name__ == '__main__':
    ui = UI()
    curses.wrapper(ui.run)

