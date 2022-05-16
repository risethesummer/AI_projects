import timeit

#https://docs.python.org/3/library/itertools.html
def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def read(path):
    with open(path, 'r') as file:
        lines = file.readlines()
        matrix = []
        for l in lines:
            temp = []
            for w in l.split(' '):
                if w[0].isdigit():
                    temp.append(int(w))
                else:
                    temp.append(-1)
            matrix.append(temp)
        return matrix


def printMatrix(matrix, redSlots):
    size = len(matrix)

    for r in range(size):
        temp = ""
        for c in range(size):
            if (r, c) in redSlots:
                temp += 'red '
            else:
                temp += 'green '
        print(temp)


def translateNumToPosition(num, size):
    return (int(num/size), num%size)


def getAdjacentGreen(row, col, size):
    
    if row == 0 or row == size - 1 or col == 0 or col == size - 1:
        if row == col or row == (col - size + 1) or col == (row - size + 1):
            return 5
        return 7
    return 10
    

def checkDone(matrix, redSlots):
    size = len(matrix)
    for row in range(size):
        for col in range(size):
            if matrix[row][col] != -1:
                totalGreenNei = getAdjacentGreen(row, col, size)
                for slot in redSlots:
                    #Adjacent
                    if abs(slot[0] - row) <= 1 and abs(slot[1] - col) <= 1:
                        totalGreenNei -= 1
                if totalGreenNei != matrix[row][col]:
                    return False
    return True


def bruteForce(matrix):

    redSlots = []

    size = len(matrix)

    baseCombine = range(size ** 2)

    c = 0

    #Till not remaining red slots
    for count in range(size ** 2):

        for slot in combinations(baseCombine, count):

            redSlots.clear()

            for pos in slot:
                redSlots.append(translateNumToPosition(pos, size))
            
            print(redSlots)
            
            c += 1
            if checkDone(matrix, redSlots):
                print("States: ", c)
                return True, redSlots

    return False, None


def main():
    matrix = read("input.txt")

    start = timeit.default_timer()
    result, redSlots = bruteForce(matrix)
    stop = timeit.default_timer()

    print('Time: ', stop - start)
    if result:
        printMatrix(matrix, redSlots)
    return

if __name__ == '__main__':
    main()