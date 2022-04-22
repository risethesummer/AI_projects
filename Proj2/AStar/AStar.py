from state import State
from storeStates import StoreStates

def AStar(matrix):

    #Initial the first state (no red nodes)
    currentState = State(matrix)
    
    #Frontier to store nodes
    frontier = StoreStates()
    expanded = StoreStates()
    #Initial start node
    frontier.addState(currentState)

    while not frontier.isEmpty():
        
        #Pop the min state from the frontier
        currentState: State = frontier.popMin()

        yield currentState

        #Goal test
        if currentState.getHeuristic() == 0 and currentState.checkGoal():
            return

        oldHeu = currentState.getHeuristic()

        for nextRed in currentState.getSuccesorRedSlots():

            (canSet, stopOffset) = currentState.setColor(nextRed[0], nextRed[1])

            if canSet:
                #If the node is not in expanded list
                if currentState not in expanded and currentState not in frontier:
                    
                    #Create new state
                    successor = State(currentState)
                    frontier.addState(successor)
            
            #Recover state
            #Color the position green
            currentState.setColor(nextRed[0], nextRed[1], False, stopOffset)
            #Recover heuristic
            currentState.setHeuristic(oldHeu)

        #Push to expanded list
        expanded.addState(State(currentState))