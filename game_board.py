from config import MIN_BOARD_SIZE, MAX_BOARD_SIZE, ALLOWED_LETTERS


class GameBoard:
    
    def __init__(self, size):
        """
    Creates the game board with the chosen size.
    
    Args:
        size = the size of the board (NxN)
    """
        if size < MIN_BOARD_SIZE or size > MAX_BOARD_SIZE:
            raise ValueError(f"Board size must be between {MIN_BOARD_SIZE} or {MAX_BOARD_SIZE}")
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]

    def is_valid_coordinate(self, row, col):
        """
        Check if the provided row and col are in the boundaries of the board
        Args:
            row: row index
            col: column index
        Returns:
            bool: True if in bounds, false if not
            """
        return 0 <= row < self.size and 0 <= col < self.size
            
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
        if letter not in ALLOWED_LETTERS:
            print(f"Invalid letter: {letter}. Only {ALLOWED_LETTERS} are allowed.")
            return False
        
        if not self.is_valid_coordinate(row, col):
            print(f"Invalid coordinates: ({row}, {col}). Must be within the board size {self.size}.")
            return False
        
        if self.grid[row][col] != " ":
            print(f"Space ({row}, {col}) is already occupied.")
            return False
        
        self.grid[row][col] = letter
        return True

    def get_placed_letter(self, row, col):
        """
        Gets the letter that was placed on the board. Returns empty if no letter was placed
        
        args:
            row: row index
            col: column index
        returns:
            str: letter at specific location or " " if no letter is placed or coordinates are invalid
        """
        if self.is_valid_coordinate(row, col):
            return self.grid[row][col]
        #print(f"Invalid access at: ({row}, {col}). Returning empty string.")
        return " "  
    
    # check if board is full
    def is_board_full(self):
        """
        Check if there are no empty spaces left on the board

        Returns:
            bool: True if board is full, false if it isn't
        """
        return all(cell !=" " for row in self.grid for cell in row)
    
    def reset(self):
        """
        Reset the board to empty
        """
        self.grid = [[" " for _ in range(self.size)] for _ in range(self.size)]
    
    