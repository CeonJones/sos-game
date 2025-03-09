import pytest
from game_board import GameBoard

@pytest.fixture
def board():
    """Create a new 3x3 game board for testing."""
    return GameBoard(3)

def test_board_size3(board):
    """Test valid size of the game board."""
    assert board.size == 3 # manual implementation
    
def test_board_size15(board):
    """Test invalid size of the game board."""
    board = GameBoard(15)
    assert board.size == 15 #manual implementation



def test_place_letter_success(board):
    """Test placing a letter in an empty space."""
    assert board.place_letter(0, 0, "S") == True
    assert board.get_placed_letter(0, 0) == "S" # function changed to get_placed_letter

def test_place_letter_occupied(board):
    """Test placing a letter in an already occupied space."""
    board.place_letter(1, 1, "O")
    assert board.place_letter(1, 1, "S") == False  # Should not overwrite

def test_place_letter_out_of_bounds(board):
    """Test placing a letter outside board boundaries."""
    assert board.place_letter(5, 5, "S") == False  # Should return False

def test_get_letter_out_of_bounds(board):
    """Test getting a letter outside board boundaries."""
    assert board.get_placed_letter(5, 5) == " "  # Should return an empty space

def test_reset_board(board):
    """Test resetting the board clears all letters."""
    board.place_letter(2, 2, "O")
    board.reset()
    assert board.get_placed_letter(2, 2) == " "
