#Author github: @jazreen
#Date: August 2023

import numpy as np
import sys
sys.setrecursionlimit(100000)

#find an empty cell (row by row)
def find_empty(matrix, nrow, ncol):
    while matrix[nrow][ncol] != 0:
        ncol += 1

        if (ncol == 9):
            ncol = 0
            nrow += 1
            
            if (nrow == 9):
                ncol, nrow = -1, -1 #rethink this #update: incorrect. this is the syntax for accessing last cell of array in python. leads to infinite loop
                print("no remaining empty cell")
                print("Sudoku solved!")
                break 
            
    print(nrow, ncol) #check1
    return nrow, ncol

#check whether chosen value meets criteria
def choose_val(matrix, nrow, ncol, up_bound):
    for i in range (up_bound, 10):
        #matrix[nrow][ncol] = i
        if (check_row(matrix, nrow, i) == False
            and check_col(matrix, ncol, i) == False
            and check_square(matrix, nrow, ncol, i) == False):
            print(i) #check3 - no. printed
            return i #if the perfect match has been found, return the perfect match
        
    return 0 #if no suitable value has been found, keep the current cell empty so return 0 (to be used in another function)

#to be completed
#to set values and backtrack if needed
def backtrack(matrix, row, col, up_bound, visited_cells):

    new_row, new_col = find_empty(matrix, row, col)
   # print(f'nrow: {new_row}')
    # print(f'ncol: {new_col}')
      #base case
    if (new_row == -1 and new_col == -1): #means we have reached the end of the matrix
        return matrix

    #stack implemented to keep a record of all the empty cells- LIFO system
    #tuple used to store a pair of coordinates for each cell -- SEE CORRECTION BELOW
    #Tuple is non-mutable, I have now changed it to a list

    visited_cells.append((new_row, new_col))
    print(new_row, new_col) #check2
    
    if (new_row == -1 and new_col == -1):
        return matrix
    
    val = choose_val(matrix, new_row, new_col, up_bound)
    print(val) #check4 - prints 0 - possible issue with check_val function [SOLVED]

    if (val == 0): #no suitable value found
        matrix[new_row][new_col] = val

        if not visited_cells: #if the list is empty
            print("No solutions \n")
            return matrix

        else: #list not currently empty
            visited_cells.pop() #getting rid of the current cell from record
            matrix, old_row, old_col, up_bound, visited_cells = pop_prev_coord(matrix, visited_cells, up_bound)
        
            if (up_bound >= 10):
                matrix, old_row, old_col, up_bound, visited_cells = pop_prev_coord(matrix, visited_cells, up_bound)
            
            if (old_row == -1 and old_col == -1):
                return matrix

            return backtrack(matrix, old_row, old_col, up_bound, visited_cells) #issue detected: what if up bound is 9? you gotta return to previous still

        #possible issue: we're stuck in infinite recursion because when youre returning to the previous spot,
        #there's no guarantee that choose_val is giving you a new value. So you're stuck repeating the same value
        #ideally integrate the choose_val function to this function

        #current logic doesnt go beyond first recursion because there's no saved locations of visited cells, hence stuck in an infinite loop
        #use stack pop and append to store and collect values [DONE]
        

    else:
        matrix[new_row][new_col] = val
        up_bound = 1

        return backtrack(matrix, new_row, new_col, up_bound, visited_cells)


def pop_prev_coord(matrix, visited_record, up_bound):
                
    if not visited_record: 
        print("No solutions \n")
        old_row, old_col = -1, -1
        return (matrix, old_row, old_col, up_bound, visited_record)
    
    else: 
        old_row, old_col = visited_record.pop() #retrieve previous cell from record (to find a new value for that cell)
        upper_bound = matrix[old_row][old_col] + 1 #we will now look for values > what was the previous recorded value 
        matrix[old_row][old_col] = 0 #setting it back to zero so its picked up by the find_empty matrix during recursion

    return (matrix, old_row, old_col, upper_bound, visited_record)


#check row function
def check_row(matrix, nrow, i):
    if i in matrix[nrow]:
        print(f"row:{i}")
        print('True1')
        return True
    else:
        print('False1')

        return False

#check column function
def check_col(matrix, ncol, i):
    #extract the column
    col_ext = np.take(matrix, ncol, axis = 1) #axis = 0 used to extract rows
    if i in col_ext:
        print(i)

        print('True2')

        return True
    else:
        print('False2')

        return False
        
#check each box (3x3) function
def check_square(matrix, nrow, ncol, int):
    #m = main
    mrow = main_row_col(nrow)
    mcol = main_row_col(ncol)

    for i in range(0, 3): #i = row
        #outer loop moves us to a new row 
        for j in range(0, 3): #j = col
            #inner loop checks each row (each row = 3 col)
            if matrix[mrow + i][mcol + j] == int: #issue detecetd: incorrect condition, we should be checking with proposed integer not the value at that position i.e. 0
                print(f'True3, {mrow+i} and {mcol+j}')

                return True    

    print('False3')
        
    return False

#returns the top leftmost row/col number of the 3x3 square the current spot exists in
def main_row_col(row_col): #input = row or column number of current spot
    if row_col in [0, 1, 2]:
        return 0
    
    if row_col in [3, 4, 5]:
        return 3

    if row_col in [6, 7, 8]:
        return 6


if __name__ == "__main__":
    #the game to solve
    original = [[5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]]
    #needed 10,000 recursion limit
    
    super_easy = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 0],
            [2, 8, 7, 4, 0, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 0]
            ] 
    
    easy = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]


    hard = [
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ]


    cell_record = list() #coordinates of all the cells that have been filled up so far


    game = backtrack(easy, 0, 0, 1, cell_record)
    print(easy)