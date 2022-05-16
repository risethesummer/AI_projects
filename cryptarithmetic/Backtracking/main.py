from Utils import *
import time

#postfix: is the left side of the calculation (includes operators and words) after converting to postfix. Used for calculating.
#right_side: contains result words (at the right side)
#addend_words: left_side with words only (not includes operators)
#Alphabet (in Ultils.py file): A dictionary class contains all unique letters. Keys are letters (char) and Values are numbers (default: -1)
domain = [0,1,2,3,4,5,6,7,8,9]
right_side = ""
addend_words = []
postfix = []

#this function helps in calculating
def Calculate(postfix: str, curr_col: int):
    stack = [] 

    for i in range(len(postfix)):
        if IsOperator(postfix[i][0]):# is operator pop 2 numbers to calculate
            num1 = stack.pop()
            num2 = stack.pop()
            stack.append(Calc(num1,num2, postfix[i][0]))
        else:
            number = ""
            #This loop, which takes all number from current column to the right, would help avoid carrying and multiplication problems.
            #By adding numbers like adding a char to a string number then converts to integer number.
            for j in reversed(range(curr_col, 0)):
                if j + len(postfix[i]) >= 0: # This condition helps avoid the smaller word (small word's length) being out of the index
                    number = str(Alphabet[postfix[i][j]]) + number
                else: break
            stack.append(int(number))
    
    # We just need the digit that is at current column so other digits will be abandoned
    return stack.pop()

#the main algorithm using backtracking. If result is found --> return, no more investigation
def solveProblem(curr_row: int, curr_col: int):
    global addend_words, right_side, postfix

    #Current column may beyond the length of small words so this loop moves to the next row to find long enough word
    #Note that these words are in the left side.
    while curr_row < len(addend_words) and curr_col + len(addend_words[curr_row]) < 0: 
        curr_row+=1

    #If current column is beyond all left-side words --> end of rows in addend_words.
    if curr_row == len(addend_words):
        #and the result word.
        if curr_col + len(right_side) < 0:
            #So if the left most letter of the result word is not == 0 and -1(not assigned) then return
            if Alphabet[right_side[0]] != 0 and Alphabet[right_side[0]] != -1: return True
            return False
    
    #This part is when we are trying to assign a letter in the left side 
    if curr_row < len(addend_words): # AA+BB=CC
        
        if Alphabet[addend_words[curr_row][curr_col]] != -1: #assigned
            #recur the next row
            if(solveProblem(curr_row + 1,curr_col)): return True
        else:# Find the suitable number to assign
            for i in range(len(domain)):
                if domain[i] != -1:
                    # could_be_assigned is to check if the left most letter of the word is going to be assigned 0
                    if domain[i] == 0 and could_be_assigned(addend_words,right_side, addend_words[curr_row][curr_col]) == False: continue
                    
                    Alphabet[addend_words[curr_row][curr_col]] = domain[i]
                    domain[i] = -1

                    #recur the next row
                    if solveProblem(curr_row + 1,curr_col): return True

                    #Undo the assignment
                    domain[i] = Alphabet[addend_words[curr_row][curr_col]]
                    Alphabet[addend_words[curr_row][curr_col]] = -1
            # No suitable number --> return False
            return False
    
    else: # This part is when we trying to assign result letter after calculating

        sum_ =  Calculate(postfix, curr_col)
        
        if sum_ < 0:
            if curr_col + len(right_side) <= 0: return False
            
            carry = pow(10, curr_col*-1)
            sum_ += carry
            while(sum_ < 0):
                sum_ -= carry
                sum_ += carry + carry
                carry += carry
    
        sum_ = int(sum_/pow(10,curr_col*-1 - 1))

        if Alphabet[right_side[curr_col]] == sum_ % 10: #if letter is assigned -> recur to next column with the top most row
            if solveProblem(0, curr_col - 1): return True

        #if letter is not assigned and the result of the calculation is available in domain
        elif Alphabet[right_side[curr_col]] == -1 and sum_ % 10 in domain: 
            #assign to it
            Alphabet[right_side[curr_col]] = sum_ % 10
            domain[sum_ % 10] = -1

            #recur to the next column with the top most row
            if solveProblem(0, curr_col - 1): return True

            #undo the assignment
            domain[sum_ % 10] = sum_%10
            Alphabet[right_side[curr_col]] = -1
    return False


def Solution():
    # First checking input, if unique letters are beyond the domain size (> 10)
    if len(Alphabet) > len(domain): return False

    #Try solve problem
    if solveProblem(0, -1): return True
    else: return False

def main():
    
    global postfix, right_side, addend_words
    

    left_side, right_side = readFile("input.txt")
    addend_words = separate_words(left_side)
    postfix = convert_toPosfix(left_side)

    #main part (try solving)
    start_time = time.time() #start recording time
    result = Solution()
    end_time = time.time() #end recording time
    
    #The final result
    if result:
        #Problem has been solved --> print results including solving time, calculation.
        print (Alphabet,"\nTime consumed: " + str(end_time-start_time) + 's')
        result_str = convert_result_toString()
        print("Result:", result_str)
        print("Detailed calculation:", convert_toCaculation(left_side, right_side))
        
        #Save file
        Write_file("output.txt", result_str[result_str.index('=') + 1:])
        print("File has been saved")
    else: print("No solution found", str(end_time-start_time) + 's') #Can't solve the problem
    

if __name__ == "__main__":
    main()