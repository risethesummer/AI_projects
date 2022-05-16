from operand import Operand
from heapq import *

class PriQueue:


    def __init__(self, maxSize):
        self._queue = []
        self._maxSize = maxSize


    def getQueue(self):
        return self._queue

    def empty(self):
        return len(self._queue) == 0

    def __len__(self):
        return len(self._queue)

    def checkCanAdd(self, total):

        return len(self._queue) < self._maxSize or self._queue[0][0] < total

    def push(self, item: list[int, Operand]):

        if len(self._queue) == self._maxSize:
            self.pop()
        heappush(self._queue, [item[0], item[1].copy()])


    def pop(self):

        if len(self._queue) > 0:
            return heappop(self._queue)
        return None