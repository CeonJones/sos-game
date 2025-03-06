from game_board import GameBoard

class SOSGame:
    def __init__(self, size):
        """
        Start game board with the size chosen by player
        
        Args:
            size: default size (default is 3x3)
        """
        self.board = GameBoard(size)
        self.current_player = "Blue"

    def place_letter(self, row, col, letter):
        """
        Handles letter placement and turn switching
        
        Args:
            row: row index
            col: column index
            letter: letter to place
        """
        if self.board.place_letter(row, col, letter):
            # Switch player after correct placement
            self.current_player = "Red" if self.current_player == "Blue" else "Blue"
            return True
        return False
    
    def reset(self):
        self.board.reset()
        self.current_player = "Blue"