#Author github: @jazreen
#Date started: August 2023

import numpy as np
import sys
from tabulate import tabulate

sys.setrecursionlimit(100000) #changing python's recursion depth

class solve_sudoku():
    def __init__(self, matrix, row, col, up_bound, visited_cells):
        self.matrix = matrix
        self.row = row
        self.col = col
        self.up_bound = up_bound
        self.visited_cells = visited_cells

    #find an empty cell (checked row by row)
    #note: we only check for empty cells from AFTER the last visited cells. We dont repeat from the beginning
    def find_empty(self, matrix, nrow, ncol):
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
    def choose_val(self, matrix, nrow, ncol, up_bound):
        for i in range (up_bound, 10):
            #matrix[nrow][ncol] = i --no, dont save the value just yet
            if (self.check_row(matrix, nrow, i) == False
                and self.check_col(matrix, ncol, i) == False
                and self.check_square(matrix, nrow, ncol, i) == False):
                return i #if the perfect match has been found, return the perfect match
            
        return 0 #if no suitable value has been found, keep the current cell empty so return 0 (to be used in another function)
    
    #to set values and backtrack if needed
    def backtrack(self, matrix, row, col, up_bound, visited_cells):
        new_row, new_col = self.find_empty(matrix, row, col)
        
        #base case
        if (new_row == -1 and new_col == -1): #means we have reached the end of the matrix
            return matrix
        #stack implemented to keep a record of all the empty cells- LIFO system
        #tuple used to store a pair of coordinates for each cell 
        visited_cells.append((new_row, new_col))
        
        if (new_row == -1 and new_col == -1):#we reached end of matrix - solved!
            return matrix
        
        val = self.choose_val(matrix, new_row, new_col, up_bound) 
        if (val == 0): #no suitable value found
            matrix[new_row][new_col] = val
            if not visited_cells: #if the list is empty
                print("No solutions \n")
                return matrix
            else: #list not currently empty
                visited_cells.pop() #getting rid of the current cell from record
                matrix, old_row, old_col, up_bound, visited_cells = self.pop_prev_coord(matrix, visited_cells, up_bound)
            
                if (up_bound >= 10): #pop one more cell (go back further) if the problem couldnt be fixed in this cell (we exhausted possible solutions 1-9)
                    matrix, old_row, old_col, up_bound, visited_cells = self.pop_prev_coord(matrix, visited_cells, up_bound)
                
                if (old_row == -1 and old_col == -1): #we reached end of matrix - solved!
                    return matrix
                return self.backtrack(matrix, old_row, old_col, up_bound, visited_cells) 
        else:
            matrix[new_row][new_col] = val
            up_bound = 1
            return self.backtrack(matrix, new_row, new_col, up_bound, visited_cells)
    
    #pops and gets coords/value of last visited cell as long as the stack is not empty
    def pop_prev_coord(self, matrix, visited_record, up_bound):
                    
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
    def check_row(self, matrix, nrow, i):
        if i in matrix[nrow]:
            return True
        else:
            return False
    
    #check column function
    def check_col(self, matrix, ncol, i):
        #extract the column
        col_ext = np.take(matrix, ncol, axis = 1) #axis = 0 used to extract rows
        if i in col_ext:
            return True
        else:
            return False
            
    #check each box (3x3) function
    def check_square(self, matrix, nrow, ncol, int):
        #m = main
        mrow = self.main_row_col(nrow)
        mcol = self.main_row_col(ncol)
        for i in range(0, 3): #i = row
            #outer loop moves us to a new row 
            for j in range(0, 3): #j = col
                #inner loop checks each row (each row = 3 col)
                if matrix[mrow + i][mcol + j] == int: 
                    return True     
        
        return False
    
    #returns the top leftmost row/col number of the 3x3 square the current spot exists in
    def main_row_col(self, row_col): #input = row or column number of current spot
        if row_col in [0, 1, 2]:
            return 0
        
        if row_col in [3, 4, 5]:
            return 3
        if row_col in [6, 7, 8]:
            return 6

######################################################################################################################################
#used by main function if user decides to upload their own file/matrix
def upload_file(name_file):

    #incorporating file I/O options - has to be in the specified format
    file = open(name_file, "r")
    line_list = list(file.readlines()) #readlines() reads every line of the file as a separate list--> line_list = list of such lists
    file.close() #remember to close the file!

    file_game = list()

    for line in line_list: #modify each line first
        clean_line = line.rstrip('\n').split(", ") #remove newline then split each linee by ", " i.e. comma and space
        #this gives another list of lists, clean_line, where each charcter is a separate list 

        new_row = list()
        for char in clean_line: #modify each character in the line
            num = int(char) #convert each character to an integer
            new_row.append(num) #append the integers together into a new list (so now we have one list per line of matrix)
        
        file_game.append(new_row) #append the lines to form the full matrix
        #by this point the matrix produced should look like the one in samples
    
    return file_game


if __name__ == "__main__":
    cell_record = list() #coordinates of all the cells that have been filled up so far
    #sample solver tests
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

    #ask the user how they'd like to proceed and act accordingly
    answer = None
    while (answer != 'f' and answer != 's'): #keep asking for input until user chooses file or sample
        answer = input("Welcome to the Sudoku Solver! Would you like to try your own matrix or use a sample? Press f to use your own matrix and s for sample options: ")
        
        match answer:
            case 'f': #case file
                print("To use your own matrix, ensure that the file is a .txt and that the matrix is formatted as below: \n"
                "0, 3, 4, 6, 7, 8, 9, 1, 2\n"
                "6, 7, 2, 1, 9, 5, 3, 4, 8\n"
                "1, 9, ...................\n"

                "i.e. just a 9x9 matrix of numbers, each separated by a comma and space, and newline (enter) at the end of each line/row")
                file_name = input("**Please enter the name of the file you'd like to use (name must end with .txt): ")
                unsolved_game = upload_file(file_name) #game.txt (for my use)

            case 's': #case sample - let user choose difficulty level
                print("Select which sample you'd like to try.\n"
                      "Press o for original and h for hard:")
                sample_choice = input("") 
                
                match sample_choice:
                    case 'o': #case original
                        print("Unsolved Original matrix:")
                        print(tabulate(original, tablefmt='grid'))
                        print("Solved Original matrix:")
                        unsolved_game = original

                    case 'h': #case hard
                        print("Unsolved Hard matrix:")
                        print(tabulate(hard, tablefmt='grid'))
                        print("This may take a while. Solved Hard matrix:")
                        unsolved_game = hard

                    case default: unsolved_game = None
             
            case default: print("Try again.... \n") #neither file nor sample chosen
    
    
    if (unsolved_game != None): #as long as the choice made was as asked
        game = solve_sudoku(hard, 0, 0, 1, cell_record) #change first input to change matrix to solve
        solved_matrix = game.backtrack(game.matrix, game.row, game.col, game.up_bound, game.visited_cells) #gives us the grid to print
        print(tabulate(solved_matrix, tablefmt='grid')) #prints a pretty grid instead of a list of lists

    else:
        print("Program terminating....\n"
              "Have a good day!")

   
    

