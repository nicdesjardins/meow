
'''
To do:
- figure out how to get scrolling working as that's a hangup for a bunch of things.

'''

import curses
import os
from threading import Thread
from enum import Enum

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

    text = []
    
    def __init__(self, userInputHandler = None):
        self.userInputHandler = userInputHandler

    def start(self, userInputHandler = None):
        if userInputHandler != None:
            self.userInputHandler = userInputHandler
        
        curses.wrapper(self.run)

    def setBoundaries(self):
        pass
        #    self.width, self.height = self.getDimensions()
        
    def run(self, window):

        self.window = window
        #self.setBoundaries()
        
        self.screen = curses.initscr()
        curses.init_pair(self.WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(self.BLUE_ON_WHITE, curses.COLOR_BLUE, curses.COLOR_WHITE)
        
        self.screen.bkgd(' ', curses.color_pair(self.BLUE_ON_WHITE))
        
        self.createInputWin()
        self.createOutputWin()
        
        self.input_thread = Thread(target=self.inputThread).start()

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
    
    def resizeInputWin(self):
        self.inputWin.resize(self.inputHeight, self.inputWidth)
        
    def resizeOutputWin(self):
        self.outputWin.resize(self.outputHeight, self.outputWidth)
        
    def createOutputWin(self):
        self.outputWin = curses.newpad(self.outputHeight, self.outputWidth)
        self.outputWin.scrollok(True)
        self.outputWin.idlok(True)

        self.outputWin.bkgd(' ', curses.color_pair(self.WHITE_ON_BLUE))
        self.outputWin.border()
        self.refreshOutputWin()
        
    def createInputWin(self):
        self.inputWin = curses.newpad(self.inputHeight, self.inputWidth)
        self.refreshInputWin()
        
        self.inputWin.bkgd(' ', curses.color_pair(self.BLUE_ON_WHITE))
        self.inputWin.border()
        
        self.resetInput()

    #def scroll = 0
    def pad = []
    def show_from_index = 0
    def show_to_index = 0
    
    def addStringToOutput(self, string):
        pad.append(string)
        
        if self.outY + 2 >= self.height - self.INPUT_HEIGHT:
            self.outputScroll += 2
        
        self.outputWin.addstr(self.outY, self.outX, string)
        self.refreshOutputWin()
        self.outY += 2
        self.screen.move(self.inYScr, self.inXScr)
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
    
    def inputThread(self):
        while True:
            try:
                ch = self.screen.getch()
                self.input_str += chr(ch)

                if self.hitEnterKey(ch):
                    if self.input_str.strip() != '':
                        if self.userInputHandler != None:
                            self.userInputHandler(self.input_str.strip())
                    self.resetInput()
                elif ch == curses.KEY_RESIZE:
                    print("hello?")
                    
                    self.setBoundaries()
                    self.addStringToOutput(
                        "resize triggered "
                        +"h: "+ str(self.height)
                        + "; w: "+str(self.width)
                    )
                    self.resizeOutputWin()
                    self.resizeInputWin()
                    self.refreshOutputWin()
                    self.refreshInputWin()
                    self.screen.refresh()
                
            except Exception as ex:
                pass

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
        
    def resetInput(self):
        self.inYScr = (self.height - self.INPUT_HEIGHT) + 1
        self.inXScr = 1
        self.input_str = ''
        self.refreshInputWin()
        self.screen.move(self.inYScr, self.inXScr)
        
    def hitEnterKey(self, ch = None):
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
