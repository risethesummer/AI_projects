from typing import Generator
from redSlots import RedSlots

class State:
    '''
    Represents a state when searching
    '''

    #Number of adjacent green nodes need to have
    numbers = []
    conditionSlots = []

    #Initial from matrix got from input files
    def __init__(self, args):

        #Copy constructor
        if isinstance(args, State):
            
            self._heuValue = args.getHeuristic()
        
            self._redSlots =  RedSlots(args.getRedSlots())

            #Copy to avoid affecting the old one
            temp = args.getAdjGreen()
            self._eachAdjGreen = temp.copy()
            for i in range(len(temp)):
                self._eachAdjGreen[i] = temp[i].copy()

        #First state -> called from get file process
        else:
            
            #H(n)
            self._heuValue = 0
            #No red slots
            self._redSlots = RedSlots()

            State.numbers = args

            #The matrix representing the adjacent green nodes of each node
            self._eachAdjGreen = []

            size = len(args)

            for row in range(0, size):
                
                #Used for the first state -> next states don't generate numbers list
                rowGreen = []

                for col in range(0, size):
                    
                    #Maximum
                    realGreen = 9

                    #On the borders
                    if row == 0 or row == size - 1 or col == 0 or col == size - 1:
                        #Corner
                        if row == col or row == abs(col - size + 1) or col == abs(row - size + 1):
                            #Four green nodes for the corner postions
                            realGreen = 4
                        else:
                            #6 green nodes for the positions standing on the border
                            realGreen = 6
                    
                    rowGreen.append(realGreen)
                    
                    #Does not need condition
                    if args[row][col] != -1:
                        State.conditionSlots.append((row, col))
                        #The formula of calculating heuristic: real - need
                        self._heuValue += (rowGreen[-1] - args[row][col])
                
                self._eachAdjGreen.append(rowGreen)
            

    @classmethod
    def getNumbers(cls):
        return cls.numbers


    def __eq__(self, other):
        return self._redSlots == other.getRedSlots() 


    def hash(self) -> int:
        a = self._redSlots.hash()
        return a


    def getAffectedAtPosition(self, row, col, found):

        size = len(State.numbers)

        #Check from upper line to lower line
        for offsetRow in range(-1, 2):

            considerRow = row + offsetRow  

            #Out range of the board
            if considerRow < 0 or considerRow >= size:
                continue
            
            #From left hand side to right hand side column
            for offsetCol in range(-1, 2):

                considerCol = col + offsetCol

                #Out range of the board
                if considerCol < 0 or considerCol >= size:
                    continue
                
                #The slot is fine
                found.add((considerRow, considerCol))


    #Get the free slots of the state
    def getSuccesorRedSlots(self):

        found = set()
        for con in State.conditionSlots:
            if self.getHeuristicValueAtPosition(con[0], con[1]) != 0:
                self.getAffectedAtPosition(con[0], con[1], found)

        for foundSlot in found:
            if foundSlot not in self._redSlots:
                yield foundSlot


    def checkGoal(self):
        size = len(self._eachAdjGreen)

        for row in range(size):
            for col in range(size):
                #Not an empty cell
                if State.numbers[row][col] != -1:
                    #Not fit the condition
                    if self._eachAdjGreen[row][col] - State.numbers[row][col] != 0:
                        return False 
        
        return True


    def getHeuristic(self):

        return self._heuValue


    def getFn(self):

        return len(self._redSlots) + self._heuValue


    def getRedSlots(self):

        return self._redSlots


    def getAdjGreen(self):

        return self._eachAdjGreen


    def setHeuristic(self, val):

        self._heuValue = val

    
    def getHeuristicValueAtPosition(self, row, col):
        #empty slot
        if State.numbers[row][col] == -1:
            return 0
        return self._eachAdjGreen[row][col] - State.numbers[row][col]



    def getAdjacentGreen(self, row, col):
        size = len(State.numbers)
        if row == 0 or row == size - 1 or col == 0 or col == size - 1:
            if row == col or row == (col - size + 1) or col == (row - size + 1):
                return 4
            return 6
        return 9
    

    #Set color of a slot
    #Set new value for the heuristic and the number of adjacent green nodes (check the affected slots)
    #Return the new state is possible or not
    def setColor(self, row, col, color = True, maxStop = (2, 2)):

        size = len(State.numbers)

        if color:
            self._redSlots.addSlot(size, (row, col))
        else:
            self._redSlots.remove(size, (row, col))

        #Check from upper line to lower line
        for offsetRow in range(-1, maxStop[0]):

            considerRow = row + offsetRow  

            #Out range of the board
            if considerRow < 0 or considerRow >= size:
                continue
            
            #From left hand side to right hand side column
            for offsetCol in range(-1, maxStop[1]):

                considerCol = col + offsetCol

                #Out range of the board
                if considerCol < 0 or considerCol >= size:
                    continue
                    
                #If red color
                if color:
                    
                    oldHeu = self.getHeuristicValueAtPosition(considerRow, considerCol)
                    #Decrease the number of green adjacent nodes
                    self._eachAdjGreen[considerRow][considerCol] -= 1
                    newHeu = self.getHeuristicValueAtPosition(considerRow, considerCol)
                    
                    #Negative heuristic -> can not be used to find the solution -> False
                    if newHeu < 0:
                        #Offset used to recover state
                        return (False, (offsetRow + 1, offsetCol + 1))

                    if abs(oldHeu - newHeu) != 0:
                        #Temporarily minus the heuristic (push it again later)
                        self._heuValue -= oldHeu
                        self._heuValue += newHeu

                #If green color -> process in another place to recover heuristic -> easier and faster
                else:
                    
                    #Increase the number of green adjacent nodes
                    self._eachAdjGreen[considerRow][considerCol] += 1

        #True (not touching negative heuristic)
        #False the state is impossible
        return (True, (2, 2))
