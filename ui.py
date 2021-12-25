
'''
To do:
- figure out how to get scrolling working as that's a hangup for a bunch of things.

'''

import curses
import os
from threading import Thread
from enum import Enum
from color_pair import ColorPair

def side(Enum):
    LEFT = 1
    RIGHT = 2

class UI(object):

    INPUT_HEIGHT = 4
    WHITE_ON_BLUE = 1
    BLUE_ON_WHITE = 2
    input_str = ''
    outputScroll = 0
    outY = 1
    outX = 1
    inX = 0
    inY = 0
    text = []
    show_from_index = 0
    show_to_index = 0

    cp = ColorPair()
    
    def __init__(self, userInputHandler = None):
        self.userInputHandler = userInputHandler

    def start(self, userInputHandler = None):
        if userInputHandler != None:
            self.userInputHandler = userInputHandler
        
        curses.wrapper(self.run)
    
    def run(self, window):

        self.window = window
        
        self.screen = curses.initscr()
        curses.start_color()
        
        self.screen.bkgd(' ', self.cp.getPair(curses.COLOR_BLUE, curses.COLOR_WHITE))
        
        self.createInputWin()
        self.createOutputWin()
        
        self.input_thread = Thread(target=self.inputThread).start()
        #self.inputThread()
        self.screen.refresh()
    
    def addStringToOutput(self, string):
        self.text.append(string)

        '''
        self.outputWin.erase()
        self.outY = 0
        self.outX = 0
        for s in self.text:
            self.outputWin.addstr(self.outY, self.outX, s)
            self.outY += 1
        self.screen.refresh()
        
        #self.outputWin.
        '''
        '''
        saving this as I restart output from scratch
        if self.outY + 2 >= self.height - self.INPUT_HEIGHT:
            self.outputScroll += 2
        
        self.outputWin.addstr(self.outY, self.outX, string)
        self.refreshOutputWin()
        self.outY += 2
        self.screen.move(self.inYScr, self.inXScr)
        self.screen.refresh()
        '''
    
        
    '''
    def resizeInputWin(self):
        self.inputWin.resize(self.inputHeight, self.inputWidth)
        
    def resizeOutputWin(self):
        self.outputWin.resize(self.outputHeight, self.outputWidth)
    ''' 
    def createOutputWin(self):
        
        self.outputWin = curses.newwin(self.outputHeight, self.outputWidth, 0, 0)
        self.outputWin.bkgd(' ', self.cp.getPair(curses.COLOR_BLUE, curses.COLOR_WHITE))
        self.outputWin.border()
        
    def createInputWin(self):
        self.inputWin = curses.newwin(self.inputHeight, self.inputWidth, self.outputHeight, 0)
        self.inputWin.bkgd(' ', self.cp.getPair(curses.COLOR_WHITE, curses.COLOR_BLUE))
        self.inputWin.border()
    
    def inputThread(self):
        
        while True:
            try:
                ch = self.screen.getch()
                self.input_str += chr(ch)

                if self.isEnterKey(ch):
                    
                    if self.input_str.strip() != '':
                        if self.userInputHandler != None:
                            self.userInputHandler(self.input_str.strip())
                        self.resetInput()
                    else:
                        self.addCharToInput(ch)
                
                elif ch == curses.KEY_RESIZE:
                    self.handleResize()
                
                self.screen.refresh()
            except Exception as ex:
                pass
    
    def addCharToInput(self, ch):
        self.inputWin.addch(self.inY, self.inX, ch)
        self.input_str += chr(ch)
        self.inX += 1

    def resetInput(self):
        #self.inY = 0
        #self.inX = 0
        self.input_str = ''
        self.inputWin.erase()
        self.inputWin.refresh()
#        self.screen.move(self.inY, self.inX)
        
    def handleResize(self):
        #self.resizeOutputWin()
        #self.resizeInputWin()
        #self.refreshOutputWin()
        #self.refreshInputWin()
        self.screen.refresh()
        
    def getAnswer(self, question):
        self.answer = None
        self.addStringToOutput(question)
        self.userInputHandler = self.getAnswerUserInputHandler
        while self.answer == None:
            pass
        return self.answer
    
    def getAnswerUserInputHandler(self, string):
        self.answer = string
            
    def getOutputHeight(self):
        return self.height - self.INPUT_HEIGHT
    outputHeight = property(getOutputHeight)

    def getOutputWidth(self):
        return self.width
    outputWidth = property(getOutputWidth)

    def getInputHeight(self):
        return self.INPUT_HEIGHT
    inputHeight = property(getInputHeight)

    def getInputWidth(self):
        return self.width
    inputWidth = property(getInputWidth)

    '''
    def refreshOutputWin(self):
        pminrow = self.outputScroll
        pmincol = 0
        sminrow = 0
        smincol = 0
        smaxrow = self.height - self.INPUT_HEIGHT
        smaxcol = self.width
        self.outputWin.border()
        self.outputWin.refresh(pminrow,pmincol, sminrow,smincol, smaxrow,smaxcol)

    def refreshInputWin(self):
        pminrow = 0
        pmincol = 0
        sminrow = self.height - self.INPUT_HEIGHT
        smincol = 0
        smaxrow = self.height
        smaxcol = self.width
        self.inputWin.border()
        self.inputWin.refresh(pminrow,pmincol, sminrow,smincol, smaxrow,smaxcol)
        self.screen.refresh()
    '''
        
    def isEnterKey(self, ch = None):
        if ch == None:
            ch = self.ch
        return self.isNewline(ch)
    
    def isNewline(self, ch):
        return ch in { curses.KEY_ENTER, 10, 13}

    def getWidth(self):
        return self.getDimensions()[0]
    width = property(getWidth)
    
    def getHeight(self):
        return self.getDimensions()[1]
    height = property(getHeight)
    
    def getDimensions(self):
        size = os.get_terminal_size()
        return [size.columns, size.lines]
