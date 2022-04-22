from copy import deepcopy

class TwoWayDict:


    def __init__(self):
        self._keyToValue = {}
        self._valueToKey = [-1 for _ in range(10)]


    def getKeyToVal(self):
        return self._keyToValue

    def copy(self):
        clone = TwoWayDict()
        clone.setKeyToVal(self._keyToValue)
        return clone

    def setKeyToVal(self, dic):
        self._keyToValue = deepcopy(dic)
        for item in self._keyToValue.items():
            if item[1] is not None:
                self._valueToKey[item[1]] = item[0]
    

    def getAllChar(self):
        return tuple(self._keyToValue.keys())

    def getKeyByVal(self, val):
        return self._valueToKey[val]

    def getItems(self):
        return self._keyToValue.items()


    def __getitem__(self, key):
        return self._keyToValue.get(key, None)


    def __setitem__(self, key, val):
        self._keyToValue[key] = val
        if val is not None:
            self._valueToKey[val] = key


    def __eq__(self, other):
        if other is None:
            return True
        a = set(self._keyToValue.items())
        if len(a) == 1:
            return True
        return len(a.intersection(other.getItems())) == len(a)


    def isUsedDigit(self, digit):

        return digit in self._keyToValue.values()


    def swapValues(self, key, valToSwap):

        keySwap = self._valueToKey[valToSwap]

        valTemp = self._keyToValue[key]

        self[key] = valToSwap

        self[keySwap] = valTemp

        return keySwap

    #The functions are no use -> just to avoid error in heappush function
    def __lt__(self, other):
        return True
    
    def __le__(self, other):
        return True