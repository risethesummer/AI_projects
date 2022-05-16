from expression import Expression
from utilities import *


def IsOperator(ch):
    return ch == '+' or ch == '-' or ch == '*' or ch == '='


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

#Read a file and return the expression in postfix format
def readFile(file_path):

    with open(file_path, "r") as file:
        content = file.readline()
        #Move the right side to the left side
        content = convert_toPosfix(content.replace('=', '-'))
        return Expression(content)