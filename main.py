from gui_manager import GUIManager


class MinimalGameBoard:
    def __init__(self, size):
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]
            
    def place_letter(self, row, col, letter):
        if self.grid[row][col] == " ":
            self.grid[row][col] = letter
            return True
        return False
    

class MinimalSOSGame:
    def __init__(self):
        self.board = MinimalGameBoard(3)
        self.current_player = "Blue"
    
    def place_letter(self, row, col, letter):
        if self.board.place_letter(row, col, letter):
            self.current_player = "Red" if self.current_player == "Blue" else "Blue"
            return True
        return False

    def is_over(self):
        return False
    
    def get_winner(self):
        return None
    
    def reset(self):
        self.board = MinimalGameBoard(3)

if __name__ == "__main__":
    game = MinimalSOSGame()
    gui = GUIManager(game)
    gui.play()

