from threading import Lock, Thread
from utilities import *
from collections import deque
from time import time
from heapq import *
from priorityQueue import PriQueue
from state import State
from storeTotal import StoreTotal
from expression import Expression

MAXSTORE = 5
K = 15
storeMaps = PriQueue(K)
found = False
sidewayNow = 0
sideWaySem = Lock()
foundSemap = Lock()
storeMapsSem = Lock()
result = None


def AddState(parentState: State, total: int):

    foundSemap.acquire()
    #If find the goal -> no need to add
    if found:
        foundSemap.release()
        return
    foundSemap.release()

    temp = None
    storeMapsSem.acquire()
        #Check can add the new state
    if storeMaps.checkCanAdd(-total):
        temp = parentState.copy()
        storeMaps.push([-total, temp])
    storeMapsSem.release()

    return temp


def ThreadSearch(parentTotal: int, parentState: State):

    global sidewayNow

    minTotal = -parentTotal

    oldOnes = deque()

    for var in Expression.allChars:

        #Try with available values to get the min conflict value
        for i in range(0, 10):

            if parentState[var] != i and (i != 0 or (var not in Expression.leadChars)):
                    
                parentMap = parentState.getMap()

                #The digit is used or not
                used = parentMap.isUsedDigit(i)

                if used and parentMap[var] == 0 and (parentMap.getKeyByVal(i) in Expression.leadChars):
                    continue

                parentState.getNewTotal(var, parentMap[var], i)

                if used:
                    #Assign to caculate the expression temporarily
                    keySwap = parentMap.swapValues(var, i)
                    parentState.getNewTotal(keySwap, i, parentMap[keySwap])
                else:
                    lostVal = parentMap[var]
                    parentMap[var] = i

                curTotal = parentState.CalcExpression()

                #If reach the goal -> set found to true and return the state
                if curTotal == 0:
                    global result, found
                    foundSemap.acquire()
                    found = True
                    foundSemap.release()
                    result = parentState.getMap()
                    return

                #Access sideway var
                sideWaySem.acquire()

                #Object function
                if curTotal < minTotal or (curTotal == minTotal and sidewayNow > 0 and parentState.getMap() not in oldOnes):
                        
                    #If a sideway move
                    if curTotal == minTotal:
                        sidewayNow -= 1
                        #print(curTotal)
                    #Set new min
                    minTotal = curTotal
                    #Add the state
                    add = AddState(parentState, minTotal)
                    if add is not None:
                        if len(oldOnes) > MAXSTORE:
                            oldOnes.popleft()
                        oldOnes.append(add.getMap())

                sideWaySem.release()
                
                #Recover the parent state
                if used:
                    #If used a used digit -> Swap to retrieve the state
                    parentMap.swapValues(keySwap, parentMap[var])
                else:
                    #Assign again to retrieve the state
                    parentMap[var] = lostVal

                #Recover old total
                parentState.getNewTotal(var, i, parentMap[var])
                if used:
                    parentState.getNewTotal(keySwap, parentMap[var], i)


def BeamSearch(expressionsInput: list[Expression], maxTime = 300, sidewayEachSearch = 50, 
    maxAttempEachSearch = 200):

    global sidewayNow, storeMaps, result
    State.expression = expressionsInput
    #Store threads
    threads = deque()

    while not storeMaps.empty():
        storeMaps.pop()

    startTime = time()
    #Not run out of time
    while (time() - startTime < maxTime):
        
        sidewayNow = sidewayEachSearch

        #Initilize maps
        for _ in range(K):
            state = State(Expression.initialMap.copy(), StoreTotal(None))
            storeMaps.push([0, state])

        for ini in storeMaps.getQueue():
            CreateRandomState(ini[1].getMap(), Expression.allChars, Expression.leadChars)
            ini[1].firstCountTotal()
            count = ini[1].CalcExpression()
            #If fortunately catching the result
            if count == 0:
                return ini[1].getMap()
            #Modify heuristic value of the state
            ini[0] = -count
            

        for _ in range(maxAttempEachSearch):

            #Local maxima
            if storeMaps.empty():
                break

            while not storeMaps.empty():
                #Get state from queue
                state = storeMaps.pop()
                #Create thread for starting the state
                thread = Thread(target=ThreadSearch, args=(state))
                threads.append(thread)

            for t in threads:
                t.start()

            while len(threads) > 0:
                threads.popleft().join()

            if found:
                return result

        #Make the queue empty
        while not storeMaps.empty():
            storeMaps.pop()

    #No solution is found by the algorithm
    return None