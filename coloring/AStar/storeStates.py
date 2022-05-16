from sys import maxsize as maxInt
from collections import OrderedDict

class StoreStates:
    '''
    Store states in a frontier or expanded list\n
    Use hash function for quickly accessing states by its red positions
    '''


    def __init__(self):
        #Used as priority queue
        self._store = OrderedDict()


    def __contains__(self, state):
        
        hashPos = state.hash()
        
        if hashPos not in self._store:
            return False

        #Check for every state having the same hash
        for check in self._store[hashPos]:
            if check == state:
                return True

        return False


    def __getitem__(self, state):
        
        hashPos = state.hash()
        
        if hashPos not in self._store:
            return None

        #Check for every state having the same hash
        for check in self._store[hashPos]:
            if check == state:
                return check

        return None


    def isEmpty(self):
        return len(self._store) == 0


    def popMin(self):
        minState = None
        minFn = maxInt
        for val in self._store.values():
            for state in val:
                fn = state.getFn()
                if fn < minFn:
                    minState = state
                    minFn = fn
        
        self.removeState(minState)
        return minState


    def addState(self, state):
        hashPos = state.hash() 
        #Not exist
        if (hashPos not in self._store):
            self._store[hashPos] = []
        self._store[hashPos].append(state)
    

    def removeState(self, state):
        try:
            hashPos = state.hash()
            self._store[hashPos].remove(state)
            #If the hash has no remaining elements
            if len(self._store[hashPos]) == 0:
                self._store.pop(hashPos)
        except:
            pass