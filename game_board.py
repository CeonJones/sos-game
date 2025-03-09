class GameBoard:
    
    def __init__(self, size):
        """
    Creates the game board with the chosen size.
    
    Args:
        size = the size of the board (NxN)
    """
        if size < 3 or size > 10:
            raise ValueError("Board size must be between 3 or 10")
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
            True if letter placed, false if it isn's
        """
        if 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == " ":
            self.grid[row][col] = letter
            return True
        return False
    
    def get_placed_letter(self, row, col):
        """
        Gets the letter that was placed on the board. Returns empty if no letter was placed
        
        args:
            row: row index
            col: column index
        returns:
            Letter that was placed on board
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return " "
    
    def reset(self):
        """
        Reset the board to empty
        """
        self.grid = [[" " for _ in range(self.size)] for _ in range(self.size)]
    
    