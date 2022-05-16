import utils
from collections import namedtuple
import copy
import timeit

def create_boolMatrix(size):
    return [[0 for _ in range(size)] for _ in range(size)]

def get_combinatorics_list(depth:int, sublist:list, curr_pos:int, line:list):
    result = []
    if depth == 0:
        line_new = [line[i] for i in range(len(line))]
        result.append(line_new)
        return result

    for i in range(curr_pos, len(sublist)):
        line.append(sublist[i])
        result+=get_combinatorics_list(depth - 1, sublist, i + 1, line)
        line.pop()

    return result

def get_combinatorics(position, bool_matrix):
    posX = position.pos_x
    posY = position.pos_y
    value = position.value
    sub_list = []
    surround_cells = 0

    #surrounding
    for i in range(posX - 1, posX + 2):
        for j in range(posY - 1, posY + 2):
            if i < 0 or j < 0 or i >= len(bool_matrix) or j >= len(bool_matrix): continue
            else:
                if bool_matrix[i][j] == 2: value -= 1
                elif bool_matrix[i][j] == 1: continue
                else:
                    surround_cells+=1
                    sub_list.append((i,j))
                    bool_matrix[i][j] = 1
    
    if value < 0:
        return None
    if surround_cells < value:
        return None

    return get_combinatorics_list(value, sub_list, 0, [])

def backtracking(list_numeric: list, bool_matrix, current_cell:int, res):
    if current_cell == len(list_numeric):
        for i in range(len(bool_matrix)):
            line = []
            for j in range(len(bool_matrix)):
                line.append(bool_matrix[i][j])
            res.append(line)
        return True

    clone_matrix = copy.deepcopy(bool_matrix)
    combinatorics_list = get_combinatorics(list_numeric[current_cell], clone_matrix)
    if combinatorics_list == None: return False

    for _tuple in combinatorics_list:
        for position in _tuple:
            clone_matrix[position[0]][position[1]] = 2
        
        if(backtracking(list_numeric, clone_matrix, current_cell + 1, res)):return True
    
        for position in _tuple:#undo
            clone_matrix[position[0]][position[1]] = 1

    return False

def get_numericList(matrix):
    res = []
    
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != '.':
                position = namedtuple('position', ["pos_x", "pos_y", "value"])
                res.append(position(pos_x = i, pos_y = j, value = int(matrix[i][j])))
    return res


def solve(matrix, bool_matrix):
    res = []
    list_numeric_cell = get_numericList(matrix)
    backtracking(list_numeric_cell, bool_matrix, 0, res)
    return res

def main():
    matrix = utils.Read_file("input.txt")
    bool_matrix = create_boolMatrix(len(matrix))

    start = timeit.default_timer()
    result = solve(matrix, bool_matrix)
    stop = timeit.default_timer()

    print('Time:', stop - start)
    utils.print_matrix(result)
    
if __name__ == '__main__': main()