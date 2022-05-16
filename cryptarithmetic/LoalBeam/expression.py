from twoWayDic import TwoWayDict
from operand import Operand


class Expression:

    allChars = set()
    leadChars = set()
    initialMap = TwoWayDict()

    def __init__(self, postfix: list[str]):

        #Char: indexes store char
        self._charToOpe = {}
        self._content = []

        chars = set()
        for i in range(0, len(postfix)):
            #If an operand -> store operand instance
            if postfix[i][0].isalpha():
                self._content.append(Operand(postfix[i]))
                self.leadChars.add(postfix[i][0])    
                for char in postfix[i]:
                    chars.add(char)
                    self.allChars.add(char)
                    self.initialMap[char] = None
            #Store operator itself
            else:
                self._content.append(postfix[i])
        
        #Get index of operands containing char a specific char
        for char in chars:
            self._charToOpe[char] = []
            for i in range(len(self._content)):
                if isinstance(self._content[i], Operand) and char in self._content[i]:
                    self._charToOpe[char].append(i)


    def __getitem__(self, i) -> Operand:
        return self._content[i]

    def __contains__(self, var):
        return var in self._charToOpe

    def getContent(self) -> list:
        return self._content

    def getAffectedOpe(self, var) -> list[int]:
        return self._charToOpe[var]