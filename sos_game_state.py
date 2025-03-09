from game_board import GameBoard

class SOSGame:
    def __init__(self, size, mode="Simple Game"):
        """
        Start game board with the size and game mode chosen by player
        
        Args:
            size: default size (default is 3x3)
            mode: defualt mode (default is Simple Game)
            current_player: default player (default is Blue)
        """
        self.board = GameBoard(size)
        self.mode = mode
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
            # Switch player after successful placement
            self.current_player = "Red" if self.current_player == "Blue" else "Blue"
            return True
        return False
    
    def check_sos_after_move(self):
        """
        Check if an SOS pattern is made after each letter placement

        Returns:
            If an SOS pattern is made then True, otherwise False
        """
        # Get the board size and put all directions into list
        size = self.board.size
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


        # Check for SOS pattern in every direction
        for row in range(size):
            for col in range(size):
                letter = self.board.get_placed_letter(row, col)
                if letter == "S":
                    # Debugging: checking is an 'S' is found on the board
                    print(f" 'S' found at: ({row}, {col})")
                    
                    for row_dir, col_dir in directions:
                        # Check if there is an 'O' in the direction
                        row_dir_o, col_dir_o = row + row_dir, col + col_dir
                        # Check for second 'S' in the direction
                        row_dir_s2, col_dir_s2 = row + 2 * row_dir, col + 2 * col_dir

                        # Check if the 'O' and 'S' are in bounds
                        letter_o = self.board.get_placed_letter(row_dir_o, col_dir_o)
                        letter_s2 = self.board.get_placed_letter(row_dir_s2, col_dir_s2)

                        # Debugging: checkig 
                        print(f"Checking direction: ({row_dir}, {col_dir})")
                        print(f"Middle letter: {letter_o} and end letter: {letter_s2}")
                        #
                        if letter_o == "O" and letter_s2 == "S":
                            print(f"SOS found at: ({row}, {col})")
                            return True
        
        print("No SOS found")
        return False    
    
    def reset(self):
        """
        Resets the game board and swithches current player back top blue
        """
        self.board.reset()
        self.current_player = "Blue"