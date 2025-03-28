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
        self.score = {"Red": 0, "Blue": 0} if mode == "General Game" else None
        self.game_over = False

    def place_letter(self, row, col, letter):
        """
        Handles letter placement and turn switching
        
        Args:
            row: row index
            col: column index
            letter: letter to place
        """
        if self.board.place_letter(row, col, letter):
            # Check sos pattern before switching player
            current_player = self.current_player
            sos_found = self.check_sos_after_move(current_player, row, col)

            # Check winner in simple game mode
            if self.mode == "Simple Game" and sos_found:
                self.winner = self.current_player
                self.game_over = True
                print(f"{self.winner} wins!")
                return True
            
            # Switch player after successful placement
            if not self.game_over:
                self.current_player = "Red" if self.current_player == "Blue" else "Blue"

            # Check winer in general game mode
            if self.mode == "General Game":
                self.evaluate_end_conditions()
            
            return True
        return False
    
    def get_score(self):
        """
        Returns the current score of the game
        """
        return self.score if self.mode == "General Game" else None
    
    def check_sos_after_move(self, player, row, col): 
        """
        Check if an SOS pattern is made after each letter placement

        Returns:
            If an SOS pattern is made then True, otherwise False
        """
        # Get the board size and put all different directions into list
        size = self.board.size
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        sos_count = 0


        # Check for SOS pattern in every direction

        if self.board.get_placed_letter(row, col) != "S":
            return False
        
        for row_dir, col_dir in directions:
            r1, c1 = row + row_dir, col + col_dir
            r2, c2 = row + 2 * row_dir, col + 2 * col_dir
            if (
                self.board.get_placed_letter(r1, c1) == "O" and
                self.board.get_placed_letter(r2, c2) == "S"
            ):
                sos_count += 1
                print(f"SOS found at: ({row}, {col})")
                #sos_found = True
            
            r1_reverse, c1_reverse = row - row_dir, col - col_dir
            r2_reverse, c2_reverse = row - 2 * row_dir, col - 2 * col_dir
            if (
                self.board.get_placed_letter(r1_reverse, c1_reverse) == "O" and
                self.board.get_placed_letter(r2_reverse, c2_reverse) == "S"
            ):
                sos_count += 1
                print(f"SOS found at: ({r2_reverse}, {c2_reverse})")
            
            if sos_count > 0:
                if self.mode == "General Game":
                    self.score[player] += sos_count
                    print(f"{player} scored {sos_count} Total score: {self.score[player]}")
                elif self.mode == "Simple Game":
                    self.winner = self.current_player
                    self.game_over = True
                    print(f"{self.winner} wins!")
                return True
        return False
            #for col in range(size):
                #letter = self.board.get_placed_letter(row, col)
                #if letter == "S":
                    # Debugging: checking is an 'S' is found on the board
                    #print(f" 'S' found at: ({row}, {col})")
                    
                    #for row_dir, col_dir in directions:
                        # Check if there is an 'O' in the direction
                        #row_dir_o, col_dir_o = row + row_dir, col + col_dir
                        # Check for second 'S' in the direction
                        #row_dir_s2, col_dir_s2 = row + 2 * row_dir, col + 2 * col_dir

                        # Check if the 'O' and 'S' are in bounds
                        #letter_o = self.board.get_placed_letter(row_dir_o, col_dir_o)
                        #letter_s2 = self.board.get_placed_letter(row_dir_s2, col_dir_s2)

                        # Debugging: checking if 'O' and 'S' are found in the direction of an placed 'S' 
                        #print(f"Checking direction: ({row_dir}, {col_dir})")
                        #print(f"Middle letter: {letter_o} and end letter: {letter_s2}")
                        #
                        #if letter_o == "O" and letter_s2 == "S":
                            # Debugging: printing to console if SOS pattern found
                            #print(f"SOS found at: ({row}, {col})")

                            # Updating scores in general game mode
                            #if self.mode == "General Game":
                                #self.score[player] += 1
                                # Debugging: printing to console if SOS pattern found
                                #print(f"{player} scored! Current score: {self.score[player]}")
                            # Updating score simple game mode
                            #elif self.mode == "Simple Game":
                                #self.winner = self.current_player
                                #self.game_over = True
                                #print(f"{self.winner} wins!")
                            # Debugging: printing to console if SOS pattern found
                            #print(f"{self.current_player} wins!")
                            #return True
        
    # end of game logic in an SOS game
    def evaluate_end_conditions(self):
        """
        Check if the game shoudl end based on the game mode
        Will set self.game and self.winner if the game when needed
        """
        if self.mode == "Simple Game":
            if self.board.is_board_full() and not self.game_over:
                self.game_over = True
                self.winner = None
                print("Game over! No more moves left.")
            elif self.mode == "General Game":
                if self.board.is_board_full():
                    self.game_over = True
                    blue_score = self.score["Blue"]
                    red_score = self.score["Red"]
                    if blue_score > red_score:
                        self.winner = "Blue"
                        print("Blue wins!")
                    elif red_score > blue_score:
                        self.winner = "Red"
                        print("Red wins!")
                    else:
                        self.winner = None
                        print("It's a Draw")
                return True
        print("No SOS found")
        return False    
    
    def reset(self):
        """
        Resets the game board and swithches current player back top blue
        """
        self.board.reset()
        self.current_player = "Blue"