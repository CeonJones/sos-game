import pytest


class MinimalGameBoard:
    def __init__(self, size):
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]
            
    def place_letter(self, row, col, letter):
        if self.grid[row][col] == " ":
            self.grid[row][col] = letter
            return True
        return False
    
def test_board_creation():
    board = MinimalGameBoard(3)
    assert board.size == 3
    assert board.grid == [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

def test_place_letter():
    board = MinimalGameBoard(3)

    #place letter and check if it was placed correctly
    assert board.place_letter(0, 0, "S") == True
    assert board.grid == [["S", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    
    #try to place letter in the taken spot
    assert board.place_letter(0, 0, "O") == False
    assert board.grid == [["S", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    