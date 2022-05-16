from operand import Operand
from utilities import ConvertOperandToNumber
from twoWayDic import TwoWayDict
from expression import Expression
from copy import deepcopy

class StoreTotal(object):

    def __init__(self, total: list[int] = None):
        self._total = {}
        if total is not None:
            self._total = deepcopy(total)

    def __getitem__(self, index):
        return self._total[index]

    def __setitem__(self, index, val):
        self._total[index] = val

    def copy(self):
        return StoreTotal(self._total)


    def CaculateFirstTotal(self, expression: Expression, dic: TwoWayDict):
        content = expression.getContent()
        for i in range(len(content)):
            if isinstance(content[i], Operand):
                self._total[i] = (ConvertOperandToNumber(content[i], dic))


    def ModifyTotal(self, expression: Expression, var, oldVal: int, newVal: int):
        for affOpe in expression.getAffectedOpe(var):
            self._total[affOpe] = expression[affOpe].getNewTotalOfVar(var, self._total[affOpe], oldVal, newVal)