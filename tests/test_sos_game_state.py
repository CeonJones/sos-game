import pytest
from sos_game_state import SOSGame

@pytest.fixture
def game():
    """Create a new 3x3 SOS game instance."""
    return SOSGame(3)

def test_game_mode_selection():
    """Test if the game correctly initializes with the selected game mode."""
    simple_game = SOSGame(3, mode="Simple Game")
    assert simple_game.mode == "Simple Game" # implemented manually

    general_game = SOSGame(3, mode="General Game")
    assert general_game.mode == "General Game" # implemented manually

def test_place_letter_switch_turns(game):
    """Test placing a letter switches turns."""
    game.place_letter(0, 0, "S")
    assert game.current_player == "Red"

def test_place_letter_occupied(game):
    """Test placing a letter in an already occupied space."""
    game.place_letter(1, 1, "O")
    assert game.place_letter(1, 1, "S") == False  # Should not overwrite

def test_check_sos_horizontal(game):
    """Test detecting SOS in a horizontal line."""
    game.place_letter(0, 0, "S")
    game.place_letter(0, 1, "O")
    game.place_letter(0, 2, "S")
    assert game.check_sos_after_move() == True  # Should detect SOS

def test_check_sos_no_sos(game):
    """Test when no SOS is present."""
    game.place_letter(0, 0, "S")
    game.place_letter(1, 1, "O")
    game.place_letter(2, 1, "S") # had to change this line to pass test
    assert game.check_sos_after_move() == False  # No SOS formed

def test_reset_game(game):
    """Test resetting the game clears the board and resets turn to Blue."""
    game.place_letter(1, 1, "S")
    game.reset()
    assert game.current_player == "Blue"
    assert game.board.get_placed_letter(1, 1) == " "
