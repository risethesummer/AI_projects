Alphabet = {}

def IsOperator(ch):
    return ch == '+' or ch == '-' or ch == '*' or ch == '='

def Calc(num1,num2, operator):
    if operator == '+': return num1 + num2
    if operator == '-': return num2 - num1
    if operator == '*': return num1 * num2 

def readFile(file_path):
    file = open(file_path,"r")
    content = file.readline()
    file.close()

    if content[-1].isalpha() == False:
        content = content[:-1]

    for char in content:
        if char.isalpha():
            if char not in Alphabet:
                Alphabet[char] = -1
            
    left = content[:content.find('=')]
    right = content[content.find('=') + 1:]
    
    return left, right

#seperate operators and words --> return words only
def separate_words(input):
    result = []
    word = ""
    for char in input:
        if char.isalpha():
            word+=char
        elif IsOperator(char):
            result.append(word)
            word = ""
    result.append(word)
    return result

#This function checks all letters at the most left of words can't be = 0
def could_be_assigned(left_side, right_side, char):
    if right_side.find(char) == 0: return False #we reached the left most letter in result word

    #use a loop for suring all letters in a word is not at the left most of other words
    for line in left_side:
        if line.find(char) == 0: return False
    return True

#get priority of a operator.
def priority(operator):
    if operator == '*' or operator == '/':
        return 2
    elif operator == '+' or operator == '-':
        return 1
    return 0

def convert_toPosfix(input : str):
    queue = [] #final result (postfix)
    stack = [] #for operators and parentheses 

    i = 0
    while i < len(input):
        word = "" #contains all letters that gonna be pushed to queue

        if input[i] == '(': #if open parentheses --> always put to stack
            stack.append(input[i])

        elif input[i]==')': #if close parentheses --> pop everything except '(' from stack to queue
            while(stack[-1] != '('):
                queue.append(stack.pop())
            stack.pop()

        elif IsOperator(input[i]): #operator --> push to stack
            # if operator that is gonna push to stack has lower priority than the most top operator in stack, 
            # pop everything except '(' from stack to queue
            if len(stack) != 0 and priority(input[i]) <= priority(stack[-1]):
                while(len(stack)!= 0 and priority(input[i]) <= priority(stack[-1])):
                    queue.append(str(stack.pop()))
        
            # then push the lower operator
            stack.append(input[i])

        else: #alphabet --> push to queue
            while i < len(input) and input[i].isalpha():
                word += input[i]
                i+=1
            i-=1
            queue.append(word)
        i+=1
    
    #pop everything left in stack to queue
    while len(stack) != 0:
        queue.append(stack.pop())

    return queue


#Result part (Convert result to string in various format)
def convert_toCaculation(left_side, right_side):
    result = ""
    for char in left_side:
        if char.isalpha():
            result += str(Alphabet[char])
        else:
            result += char

    result += '='
    for char in right_side:
        result += str(Alphabet[char])
    return result

def convert_result_toString():
    letters = ""
    digits = ""
    key_list= list(Alphabet.keys())
    key_list.sort()
    for key in key_list:
        letters += key
        digits += str(Alphabet[key])

    return letters + '=' + digits
    
def Write_file(file_path: str, result: str):
    out_file = open(file_path, "w")
    out_file.write(result)
    out_file.close()
