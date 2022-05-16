def Read_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.split() for line in file]
    return lines

def print_matrix(matrix):
    for i in range(len(matrix)):
        temp = ''
        for j in range(len(matrix[i])):
            if matrix[i][j] == 2:
                temp += 'g '
            else: 
                temp += 'r '
        print(temp)