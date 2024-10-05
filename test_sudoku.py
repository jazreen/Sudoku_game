#Author github: @jazreen
#Date: January 2024

import sudoku
import unittest
matrix1 = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
            ]  #complete sudoku matrix

matrix2 = [
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ]  #unsolved sudoku matrix
 

class Test(unittest.TestCase):
    #**********************TEST find_empty*******************************
    #remember we check for empty cells row by row
    def test_find_empty1(self): #when no empty cells left
        nrow, ncol = (0,0)
        empty_row, empty_col = sudoku.find_empty(matrix1, nrow, ncol)
        self.assertEqual((empty_row, empty_col), (-1,-1), msg = "Test 1: failed oops")

    def test_find_empty2(self): #checking if it detects the first empty cell when starting from (0,0)
        nrow, ncol = (0,0)
        empty_row, empty_col = sudoku.find_empty(matrix2, nrow, ncol)
        self.assertEqual((empty_row, empty_col), (0, 1), msg = "Test 2: failed oops")
    
    def test_find_empty3(self): #checking if it ignores cells that come before the given cell (given cell = input to function)
        #e.g. if we input is (4,4) i.e. for the number 4, it should give the next 0, which is (4,7) and disregard the earlier 0s
        nrow, ncol = (4,4)
        empty_row, empty_col = sudoku.find_empty(matrix2, nrow, ncol)
        self.assertEqual((empty_row, empty_col), (4,7), msg = "Test 3: failed oops")

    #**********************TEST choose_val*******************************
    def test_choose_val(self):
        

if __name__ == '__main__':
    unittest.main()




