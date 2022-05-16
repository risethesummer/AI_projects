from pysat.solver import Glucose3
import utils
import numpy as np
import timeit

#1. 2. 3.       1^6^7^8^5 <=> -6^-7^-8^-9
#4. 5 6.
#7. 8. 3

def get_subList(pos_x: int, pos_y: int, matrix):

    sub_list = []

    for i in range(pos_x - 1, pos_x + 2):
        for j in range(pos_y - 1, pos_y + 2):
                if i < 0 or j < 0 or i >= len(matrix) or j >= len(matrix): continue  
                sub_list.append(matrix[i][j])
    return sub_list

def get_trueClauses(depth, sub_list, pos, res, line):
    if depth == 0:
        res.append([line[i] for i in range(len(line))])
        return

    for i in range(pos, len(sub_list)):
        line.append(sub_list[i])
        get_trueClauses(depth - 1, sub_list, i + 1,res, line)
        line.pop()

def generate_clause(sub_list, true_clause):

    final_clause = []

    false_clause = []
    for ele in sub_list:
        if ele not in true_clause:
            false_clause.append(ele)

    for ele in true_clause:
        temp = [false_clause[i] for i in range(len(false_clause))]
        temp.append(ele)
        final_clause.append(temp)

    for ele in false_clause:
        temp = [true_clause[i] * -1 for i in range(len(true_clause))]
        temp.append(ele*-1)
        final_clause.append(temp)
        
    return final_clause

def generate_clauses(input, sub_list):
    res = [] 
    true_clauses = [] 
    line =[]

    get_trueClauses(input, sub_list, 0, true_clauses, line)

    for i in range(len(true_clauses)):
        res += generate_clause(sub_list, true_clauses[i])
        
    return res

def solve_clauses():
    matrix = utils.Read_file("input.txt")
    position_matrix = np.reshape(range(1, len(matrix)*len(matrix)+1, 1), (len(matrix), len(matrix)))
    
    start = timeit.default_timer()
    result = []

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != '.':
                result += generate_clauses(int(matrix[i][j]), get_subList(i,j, position_matrix))

    g = Glucose3()
    for it in result:
        g.add_clause([int(k) for k in it])
    
    
    print(g.solve())
    stop = timeit.default_timer()
    print('Time: ', stop - start)

    model = g.get_model()
    print(model)

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i*len(matrix)+j+1 in model:
                print('g', end=' ')
            else:
                print('r', end=' ')
        print('')

    return result


if __name__ == '__main__':
    solve_clauses()