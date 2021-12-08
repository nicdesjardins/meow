import curses
import os

WHITE_ON_BLUE = 1
BLUE_ON_WHITE = 2

size = os.get_terminal_size()
width, height = (size.columns, size.lines)

INPUT_HEIGHT = 5

def main(window):
    
    screen = curses.initscr()
    curses.init_pair(WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(BLUE_ON_WHITE, curses.COLOR_BLUE, curses.COLOR_WHITE)

    outPad = curses.newpad(height - INPUT_HEIGHT, width)
    outPad.bkgd(' ', curses.color_pair(WHITE_ON_BLUE))
    outPad.border()
    outPad.refresh(0,0, 0,0, height - INPUT_HEIGHT, width)
    
    inPad = curses.newpad(INPUT_HEIGHT, width)
    inPad.bkgd(' ', curses.color_pair(BLUE_ON_WHITE))
    inPad.border()
    inPad.refresh(0,0, height-INPUT_HEIGHT,0, height, width)

    ''' 
    window.refresh([pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol])¶

    Update the display immediately (sync actual screen with previous drawing/deleting methods).

    The 6 optional arguments can only be specified when the window is a pad created with newpad(). 
    - The additional parameters are needed to indicate what part of the pad and screen are involved. 
    -- pminrow and pmincol specify the upper left-hand corner of the rectangle to be displayed in the pad. 
    -- sminrow, smincol, smaxrow, and smaxcol specify the edges of the rectangle to be displayed on the screen. 
    -- The lower right-hand corner of the rectangle to be displayed in the pad is calculated from the screen coordinates, since the rectangles must be the same size. Both rectangles must be entirely contained within their respective structures. Negative values of pminrow, pmincol, sminrow, or smincol are treated as if they were zero.
    '''
    

    while True:
        pass
    

if __name__ == '__main__':
    curses.wrapper(main)
