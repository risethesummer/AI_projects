from twoWayDic import TwoWayDict
from random import randint
from collections import deque

#Caculate the value of 2 variables depending the mid sign
def Caculate(a, b, sign):
    if sign == '+':
        return a + b
    elif sign == '-':
        return a - b
    return a * b

def ConvertOperandToNumber(operand, map):
    size = len(operand)
    total = 0
    for i in range(len(operand)):
        total += map[operand[size - i - 1]] * (10 ** i)
    return total

def CreateRandomState(mapCharToDigit: TwoWayDict, allChars: list, leadChars: set):

    #Mark used digits
    used = [False] * 10
    #How many numbers were taken
    count = 0

    for char in allChars:

        fail = True

        #Just has 1 digit for a lead element
        if count == 9 and (not used[0]) and char in leadChars:
            #Try to a number of a not lead element
            temp = randint(1, 9)
            while mapCharToDigit.getKeyByVal(temp) in leadChars:
                temp = randint(1, 9)
            mapCharToDigit[char] = 0
            mapCharToDigit.swapValues(char, temp)
            return

        #Till find a not used digit
        while fail:

            temp = randint(0, 9)

            if not used[temp] and (temp != 0 or (char not in leadChars)):
                mapCharToDigit[char] = temp
                used[temp] = True
                fail = False
                count += 1


def CalcByPostfix(postfix: deque):

    store = deque()

    while len(postfix) > 0:
        ele = postfix.popleft()
        #If an operator -> pop 2 values to calculate
        if isinstance(ele, str):
            first = store.pop()
            second = store.pop()
            store.append(Caculate(second, first, ele))
        #If an operand -> store it
        else:
            store.append(ele)

    return abs(store.pop())