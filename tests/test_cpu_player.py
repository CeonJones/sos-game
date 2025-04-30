import pytest
import random
from sos_game_state import SOSGame
from computer_player import MinimaxPlayer
from config import SIMPLE_MODE, GENERAL_MODE

def human_move_strategy(game: SOSGame):
    """
    Naive human: always pick 'S' at the first available empty cell.
    """
    state = game.get_state_game()
    r, c = state["legal_moves"][0]
    return {"row": r, "col": c, "letter": "S"}

def play_to_completion(game, blue_agent, red_agent):
    """
    Loop until game.game_over, calling either agent.
    Agents may be:
      - a function(game) -> move dict  (for our human_strategy)
      - a MinimaxPlayer instance    (we call .choose_move(game))
    """
    while not game.game_over:
        if game.current_player == "Blue":
            move = (blue_agent(game) 
                    if callable(blue_agent) 
                    else blue_agent.choose_move(game))
        else:
            move = (red_agent(game) 
                    if callable(red_agent) 
                    else red_agent.choose_move(game))

        assert move is not None, "Agent failed to return a move"
        assert game.place_letter(move["row"], move["col"], move["letter"]), \
            f"Failed to place {move}"

    return game

@pytest.mark.parametrize("size", [3, 5])
def test_simple_human_vs_cpu(size):
    """
    1) simple mode may draw under optimal play—just assert game_over
    """
    game = SOSGame(size, SIMPLE_MODE)
    cpu  = MinimaxPlayer(max_depth=3)

    finished = play_to_completion(game, human_move_strategy, cpu)
    assert finished.game_over

@pytest.mark.parametrize("size", [4, 6])
def test_general_cpu_vs_human(size):
    """
    2) general mode may tie on score—just assert game_over
    """
    game = SOSGame(size, GENERAL_MODE)
    cpu  = MinimaxPlayer(max_depth=3)

    finished = play_to_completion(game, cpu, human_move_strategy)
    assert finished.game_over

@pytest.mark.parametrize("size", [3, 5])
def test_simple_cpu_vs_cpu(size):
    """
    3) simple mode may draw—just assert game_over
    """
    game = SOSGame(size, SIMPLE_MODE)
    blue_cpu = MinimaxPlayer(max_depth=3)
    red_cpu  = MinimaxPlayer(max_depth=3)

    finished = play_to_completion(game, blue_cpu, red_cpu)
    assert finished.game_over

@pytest.mark.parametrize("size", [4, 6])
def test_general_cpu_vs_cpu(size):
    """
    4) general mode may tie on score—just assert game_over
    """
    game = SOSGame(size, GENERAL_MODE)
    blue_cpu = MinimaxPlayer(max_depth=3)
    red_cpu  = MinimaxPlayer(max_depth=3)

    finished = play_to_completion(game, blue_cpu, red_cpu)
    assert finished.game_over