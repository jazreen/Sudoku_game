#Author github: @jazreen
#Date: August 2023

import numpy as np
#main function
def main():

#the game to solve
    game = [[5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]]

    cell_record = [] #coordinates of all the cells that have been filled up so far


    game = backtrack(game, 0, 0, 1, cell_record)
    print(game)

#find an empty cell (row by row)
def find_empty(matrix, nrow, ncol):
    while matrix[nrow][ncol] != 0:
        ncol += 1

        if (ncol == 9):
            ncol = 0
            nrow += 1

        if (nrow == 9):
            ncol, nrow = -1, -1 #rethink this
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
            and check_square(matrix, nrow, ncol) == False):
            print(i) #check2 - no printed
            return i #if the perfect match has been found, return the perfect match
        
    return 0 #if no suitable value has been found, keep the current cell empty so return 0 (to be used in another function)

#to be completed
#to set values and backtrack if needed
def backtrack(matrix, row, col, up_bound, visited_cells):

    #base case
    if (row == -1 and col == -1):
        return matrix

    new_row, new_col = find_empty(matrix, row, col)
   # print(f'nrow: {new_row}')
    # print(f'ncol: {new_col}')


    #stack implemented to keep a record of all the empty cells- LIFO system
    #tuple used to store a pair of coordinates for each cell
    visited_cells.append((new_row, new_col))
    print(new_row, new_col) #check3 
    
    if (new_row == -1 and new_col == -1):
        return matrix
    
    val = choose_val(matrix, new_row, new_col, up_bound)
    print(val) #check4 - prints 0 - possible issue with check_val function

    if (val == 0): #no suitable value found
        matrix[new_row][new_col] = val

        if not visited_cells: 
            print("No solutions \n")
            return matrix

        else: #isempty returns true if empty
            visited_cells.pop() #getting rid of the current cell from record
            
            if not visited_cells: 
                print("No solutions \n")
                return matrix
            
            else: 
                old_row, old_col = visited_cells.pop() #retrieve previous cell from record (to find a new value for that cell)
                up_bound = matrix[old_row][old_col] + 1 #we will now look for values > what was the previous recorded value 
                matrix[old_row][old_col] = val #setting it back to zero so its picked up by the find_empty matrix during recursion
                return backtrack(matrix, old_row, old_col, up_bound, visited_cells)

        #possible issue: we're stuck in infinite recursion because when youre returning to the previous spot,
        #there's no guarantee that choose_val is giving you a new value. So you're stuck repeating the same value
        #ideally integrate the choose_val function to this function

        #current logic doesnt go beyond first recursion because there's no saved locations of visited cells, hence stuck in an infinite loop
        #use stack pop and append to store and collect values
        

    else:
        matrix[new_row][new_col] = val
        up_bound = 1

    return backtrack(matrix, new_row, new_col, up_bound, visited_cells)


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
def check_square(matrix, nrow, ncol):
    #m = main
    mrow = main_row_col(nrow)
    mcol = main_row_col(ncol)

    for i in range(0, 3): #i = row
        #outer loop moves us to a new row 
        for j in range(0, 3): #j = col
            #inner loop checks each row (each row = 3 col)
            if matrix[mrow + i][mcol + j] == matrix[nrow][ncol]:
                print('True3')

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

main()