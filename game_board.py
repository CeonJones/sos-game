class GameBoard:
    """
    Creates the game board with the chosen size.
    
    Args:
        size = the size of the board (NxN)
    """
    def __init__(self, size):
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]
            
    def place_letter(self, row, col, letter):
        """
        If space is available, put letter on the board
        
        Args:
            row: row index
            col: column index
            letter: which letter to place
        Returns:
            True if letter placed, flase if it isn's
        """
        if self.grid[row][col] == " ":
            self.grid[row][col] = letter
            return True
        return False
    
    def reset(self):
        """
        Reset the board to empty
        """
        self.grid = [[" " for _ in range(self.size)] for _ in range(self.size)]
    
    