from utilities import CalcByPostfix
from storeTotal import StoreTotal
from twoWayDic import TwoWayDict
from collections import deque


class State(object):

    expression = None

    def __init__(self, map: TwoWayDict, total: StoreTotal):
        self._map = map
        self._total = total

    def __getitem__(self, key):
        return self._map[key]

    def __eq__(self, other):
        if other is None:
            return True
        return self._map == other.getMap()

    def copy(self):
        return State(self._map.copy(), self._total.copy())

    def getMap(self):
        return self._map

    def firstCountTotal(self):
        self._total.CaculateFirstTotal(self.expression, self._map)

    def getNewTotal(self, var, oldVal, newVal):
        self._total.ModifyTotal(self.expression, var, oldVal, newVal)
    

    def CalcExpression(self):

        tempPostfix = deque()

        content = self.expression.getContent()
        for i in range(len(content)):
            if isinstance(content[i], str):
                tempPostfix.append(content[i])
            else:
                tempPostfix.append(self._total[i])
        
        #Get absolute to compare which one is nearer 0
        return CalcByPostfix(tempPostfix)

    #The functions are no use -> just to avoid error in heappush function
    def __lt__(self, other):
        return True
    
    def __le__(self, other):
        return True