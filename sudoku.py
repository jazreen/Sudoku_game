#Author github: @jazreen
#Date started: August 2023

import numpy as np
import sys
from tabulate import tabulate

sys.setrecursionlimit(100000) #changing python's recursion depth

#find an empty cell (checked row by row)
#note: we only check for empty cells from AFTER the last visited cells. We dont repeat from the beginning
def find_empty(matrix, nrow, ncol):
    while matrix[nrow][ncol] != 0:
        ncol += 1

        if (ncol == 9):
            ncol = 0
            nrow += 1
            
            if (nrow == 9): #if both row and col = 9, we have reached the end of the matrix and there are no empty cells left
                ncol, nrow = -1, -1 
                print("Sudoku solved!")
                break 

    return nrow, ncol

#check whether chosen value meets criteria
def choose_val(matrix, nrow, ncol, up_bound):
    for i in range (up_bound, 10):
        #matrix[nrow][ncol] = i --no, dont save the value just yet
        if (check_row(matrix, nrow, i) == False
            and check_col(matrix, ncol, i) == False
            and check_square(matrix, nrow, ncol, i) == False):
            return i #if the perfect match has been found, return the perfect match
        
    return 0 #if no suitable value has been found, keep the current cell empty so return 0 (to be used in another function)

#to set values and backtrack if needed
def backtrack(matrix, row, col, up_bound, visited_cells):

    new_row, new_col = find_empty(matrix, row, col)
     
    #base case
    if (new_row == -1 and new_col == -1): #means we have reached the end of the matrix
        return matrix

    #stack implemented to keep a record of all the empty cells- LIFO system
    #tuple used to store a pair of coordinates for each cell 

    visited_cells.append((new_row, new_col))
    
    if (new_row == -1 and new_col == -1):#we reached end of matrix - solved!
        return matrix
    
    val = choose_val(matrix, new_row, new_col, up_bound) 

    if (val == 0): #no suitable value found
        matrix[new_row][new_col] = val

        if not visited_cells: #if the list is empty
            print("No solutions \n")
            return matrix

        else: #list not currently empty
            visited_cells.pop() #getting rid of the current cell from record
            matrix, old_row, old_col, up_bound, visited_cells = pop_prev_coord(matrix, visited_cells, up_bound)
        
            if (up_bound >= 10): #pop one more cell (go back further) if the problem couldnt be fixed in this cell (we exhausted possible solutions 1-9)
                matrix, old_row, old_col, up_bound, visited_cells = pop_prev_coord(matrix, visited_cells, up_bound)
            
            if (old_row == -1 and old_col == -1): #we reached end of matrix - solved!
                return matrix

            return backtrack(matrix, old_row, old_col, up_bound, visited_cells) 

    else:
        matrix[new_row][new_col] = val
        up_bound = 1

        return backtrack(matrix, new_row, new_col, up_bound, visited_cells)

#pops and gets coords/value of last visited cell as long as the stack is not empty
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
        return True
    else:
        return False

#check column function
def check_col(matrix, ncol, i):
    #extract the column
    col_ext = np.take(matrix, ncol, axis = 1) #axis = 0 used to extract rows
    if i in col_ext:
        return True
    else:
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
            if matrix[mrow + i][mcol + j] == int: 
                return True     
    
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
    original = [
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]
            ]
    #needed 10,000 recursion limit
    
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
        #has the highest recursion limit

    cell_record = list() #coordinates of all the cells that have been filled up so far

    #incorporating file I/O options - has to be in a list format as above
    file = open("game.txt", "r")
    file_game = list(file.read())

    file.close()

    game = backtrack(file_game, 0, 0, 1, cell_record) #change first input to change matrix to solve

    print(tabulate(game, tablefmt='grid')) #prints a pretty grid instead of a list of lists

    #ask if person would like to try their own matrix or use one of the samples
    #act accordingly
    