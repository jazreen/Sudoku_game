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

    row = 0
    col = 0 

    row, col = find_empty(game, row, col)
    print (row, col)

#find an empty cell (row by row)
def find_empty(matrix, nrow, ncol):
    while matrix[nrow][ncol] != 0:
        ncol += 1

        if ncol == 9:
            ncol = 0
            nrow += 1

        if nrow == 9:
            ncol, nrow = 0, 0

    return nrow, ncol

#check whether value meets criteria
def check_val(matrix, nrow, ncol):
    for i in range (1,10,1):
        matrix[nrow][ncol] = i
        check_row(matrix, nrow)
#check row function
def check_row(matrix, nrow, i):
    if i in matrix[nrow]:
        return TRUE
    else:
        return FALSE

#check column function
def check_col(matrix, ncol, i):
    #extract the column
    col_ext = np.take(marix, ncol, axis = 1) #axis = 0 used to extract rows
    if i in col_ext:
        return TRUE
    else:
        return FALSE
        
#check each box (3x3) function
main()
