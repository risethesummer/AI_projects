class RedSlots:

    def __init__(self, args = None):

        self._slots = []
        self._hash = 0

        if args is not None:
            self._slots = args.getSlots().copy()
            self._hash = args.hash()


    def getSlots(self):

        return self._slots


    def __getitem__(self, index):
        return self._slots[index]


    def __len__(self):
        return len(self._slots)


    def __eq__(self, other):

        if (len(self) != len(other)):
            return False

        #Nothing different between 2 lists
        return len(set(self._slots).difference(other.getSlots())) == 0


    def hash(self) -> int:
        if len(self._slots) == 0:
            return -1
        return self._hash


    def addSlot(self, size, position):
        self._slots.append(position)
        self._hash += position[0] * size + position[1]


    def remove(self, sizeMat, position):
        size = len(self)
        for i in range(size):
            if self._slots[i] == position:
                self._slots.pop(i)
                self._hash -= position[0] * sizeMat + position[1]
                return


    def __contains__(self, position):

        for redSlot in self._slots:
            if position[0] == redSlot[0] and position[1] == redSlot[1]:
                return True
        
        return False