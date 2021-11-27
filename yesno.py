
class YesNo(object):

    YES = ['y','yes']
    NO = ['n','no']

    def ask(self, question, showYN = True):
        return input(
            question
            + (self.showYesNo() if showYN else "")
        )

    def showYesNo(self):
        return "[".join(self.YES)+"] or  "+"[".join(self.NO)+"]"
    
    def isYesOrNo(self, answer):
        return self.isValidAnswer(answer)
    
    def isValidAnswer(self, answer):
        return (
            answer in self.YES
            or answer in self.NO
        )
    
    def isYes(self, answer):
        return answer.lower() in self.YES

    def isNo(self, answer):
        return answer.lower() in self.NO
