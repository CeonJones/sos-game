from game_board import GameBoard
from config import SIMPLE_MODE, GENERAL_MODE, POINTS_PER_SOS, ALLOWED_LETTERS

class SOSGame:
    def __init__(self, size, mode="Simple Game"):
        """
        Start game board with the size and game mode chosen by player
        
        Args:
            size: default size (default is 3x3)
            mode: defualt mode (default is Simple Game)
        """
        self.board = GameBoard(size)
        self.mode = mode
        self.current_player = "Blue"
        self.game_over = False
        self.winner = None
        self.sos_sequences = []

        # Owenership grid same dimesnsions as the board
        self.owner_grid = [[None for _ in range(size)] for _ in range(size)]

        if mode == GENERAL_MODE:
            # Maintain score for each player, and move counter for there current turn
            # Also including a set to track to track moves which have already gained points
            self.score = {"Blue": 0, "Red": 0}
            self.move_counter = 0
            self.scored_moves = set()
        else:
            self.score = None # No score in simple game mode


    def place_letter(self, row, col, letter):
        """
        Handles letter placement, SOS checking, turn switching, and win conditions
        
        Args:
            row: row index
            col: column index
            letter: letter to place ('S' or 'O')
        Returns:
            bool: True if letter was placed and processed, false if not
        """
        # try to place letter
        if self.board.place_letter(row, col, letter):

            # Update owner grid to record current player move made
            self.owner_grid[row][col] = self.current_player

            # update the move counter if in general game mode
            if self.mode == GENERAL_MODE:
                self.move_counter += 1

            # Check for SOS pattern on the current move, if found, update score
            sos_found = self.check_sos_after_move(self.current_player, row, col, letter)

            # Simple mode
            if self.mode == SIMPLE_MODE:
                if sos_found:
                    self.winner = self.current_player
                    self.game_over = True
                    print(f"{self.current_player} wins!")
                    return True
                else:
                    # If no SOS and board not full, switch turns
                    if not self.board.is_board_full():
                        self.current_player = "Red" if self.current_player == "Blue" else "Blue"
                    # Check if board is full after move, then its a draw
                    if self.board.is_board_full() and not self.game_over:
                        self.game_over = True
                        self.winner = None
                        print("It's a draw! No more moves left")
            
            # General mode
            elif self.mode == GENERAL_MODE:
                if self.move_counter >= 3 or self.board.is_board_full():
                    self.move_counter = 0
                    self.current_player = "Red" if self.current_player == "Blue" else "Blue"
                    self.evaluate_end_conditions()
            return True
        return False
    
    def get_score(self):
        """
        Returns the current score of the game
        """
        return self.score if self.mode == GENERAL_MODE else None
    
    def check_sos_after_move(self, player, row, col, letter): 
        """
        Check if th move at (row, col) creates a valid SOS pattern.
        SOS checks are done in all 8 directions regardless of the letter 'S' or 'O'.
        Each move that makes an SOS pattern increases score by 1 for current player.

        Also prevents re-scoring a move that already contributed points.

        Args:
            player: player who made the move
            row: row index of the move
            col: column index of the move
            letter: letter placed ('S' or 'O')

        Returns:
            bool: True if one or more SOS patters were found, false if not
        """
        
        # If move has been scored already in general game, skip scoring.
        if self.mode == GENERAL_MODE and (row, col) in self.scored_moves:
            print(f"Move at ({row}, {col}) already scored. Skipping scoring.")
            return False
        
        # Get the board size and put all different directions into list
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)
                     ]
        #found_new_sos = False
        new_sequences = []

        for dr, dc in directions:
            # Case 1: current letter is 'S'
            if letter == "S":
                # Look ahead 2 cells for SOS pattern
                if (self.board.get_placed_letter(row + dr, col + dc) == "O" and
                    self.board.get_placed_letter(row + 2 * dr, col + 2 * dc) == "S"):
                    # Check owner of the cells matches current player
                    if (self.owner_grid[row + dr][col + dc] == player and self.owner_grid[row + 2 * dr][col + 2 * dc] == player):
                        new_sequences.append(((row, col), (row + 2 * dr, col + 2 * dc)))
                
                # Reverse check for 2 cells behind for SOS pattern
                if (self.board.get_placed_letter(row - dr, col - dc) == "O" and
                    self.board.get_placed_letter(row - 2 * dr, col - 2 * dc) == "S"):
                    if (self.owner_grid[row - dr][col - dc] == player and self.owner_grid[row - 2 * dr][col - 2 * dc] == player):
                        new_sequences.append(((row - 2 * dr, col - 2 * dc), (row, col)))

            # Case 2: current letter is 'O'
            if letter == "O":
                if (self.board.get_placed_letter(row - dr, col - dc) == "S" and
                    self.board.get_placed_letter(row + dr, col + dc) == "S"):
                    if (self.owner_grid[row - dr][col - dc] == player and self.owner_grid[row + dr][col + dc] == player):
                        new_sequences.append(((row - dr, col - dc), (row + dr, col + dc)))

            
            # If at least one new SOS is found
            if new_sequences:
                if self.mode == GENERAL_MODE:
                    # Award a point to current player
                    points = POINTS_PER_SOS * len(new_sequences)
                    self.score[player] += points
                    self.scored_moves.add((row, col))
                    print(f"{player} scored {points} points. Current score: {self.score[player]}")
                elif self.mode == SIMPLE_MODE:
                    self.winner = self.current_player
                    self.game_over = True
                    print(f"{self.winner} wins!")

                # Record sequences so GUI can use them
                self.sos_sequences.extend(new_sequences)
                return True
        return False
    
    def evaluate_end_conditions(self):
        """
        Evaluates if the game should end depending on the game mode and status of the board.
        Simple Game: Ends if the board is full or SOS is found
        General Game: End game when board is full and compare scores

        Returns:
            bool: True if end conditons met, else False
        """
        if self.board.is_board_full():
            self.game_over = True
            if self.mode == GENERAL_MODE:
                blue_score = self.score["Blue"]
                red_score = self.score["Red"]
                if blue_score > red_score:
                    self.winner = "Blue"
                    print(f"Game over! {self.winner} wins with score: {blue_score}")
                elif blue_score == red_score:
                    self.winner = None
                    print("Game over! It's a draw!")
                elif red_score > blue_score:
                    self.winner = "Red"
                    print(f"Game over! {self.winner} wins with score: {red_score}")
            elif self.mode == SIMPLE_MODE:
                self.winner = None
                print("Game over! No more moves left")
            return True
        return False
    
    def reset(self):
        """
        Resets the state of the game, score, move counter, and set scored moved
        and current player is set back to Blue.
        """
        self.board.reset()
        self.current_player = "Blue"
        self.game_over = False
        self.winner = None
        if self.mode == GENERAL_MODE:
            self.score = {"Blue": 0, "Red": 0}
            self.move_counter = 0
            self.scored_moves.clear()
        self.sos_sequences.clear()
        print("Game reset. Play again!")

    def get_state_game(self):
        """
        Returns the current game state in a dictinary format
        includes:
            - board: current board state
            - current_player: current player
            - mode: game mode
            - legal_moves: list of legal moves
            - allowed_letters: letters allowed in the game from ALLOWED_LETTERS
            - blue_score and red_score: current scores
            - game_over: boolean if game is over
            - winner: the winner of the game
        """
        legal_moves = []
        for r in range(self.board.size):
            for c in range(self.board.size):
                if self.board.grid[r][c] == " ":
                    legal_moves.append((r, c))

        state = {
            "board": self.board.grid,
            "current_player": self.current_player,
            "mode": self.mode,
            "legal_moves": legal_moves,
            "allowed_letters": sorted(list(ALLOWED_LETTERS)),
            "game_over": self.game_over,
            "winner": self.winner,
        }
        if self.mode == GENERAL_MODE:
            state["blue_score"] = self.score["Blue"]
            state["red_score"] = self.score["Red"]
        return state