class Operand():

    def __init__(self, rep):

        self._rep = rep
        self._charToPos = {}
        size = len(rep)
        for i in range(size):
            pos = size - i - 1
            char = rep[pos]
            if char not in self._charToPos:
                self._charToPos[char] = []
            self._charToPos[char].append(i)


    def __contains__(self, var):
        return var in self._rep


    def getNewTotalOfVar(self, var, total, oldVal, newVal):
        for pos in self._charToPos[var]:
            total += (newVal - oldVal) * (10 ** pos)
        return total
    

    def __getitem__(self, i):
        return self._rep[i]

    def __len__(self):
        return len(self._rep)

    def getRep(self):
        return self._rep

    def setRep(self, r):
        self._rep = r