
import curses

class ColorPair(object):
    
    colorPairCount = 0
    colorPairs = {}

    def getPair(self, fgColor, bgColor):
        pair_key = (fgColor, bgColor)
        if pair_key not in self.colorPairs:
            self.colorPairCount += 1
            curses.init_pair(self.colorPairCount, fgColor, bgColor)
            self.colorPairs[pair_key] = self.colorPairCount

        return curses.color_pair(self.colorPairs[pair_key])

