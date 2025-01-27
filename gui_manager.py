import tkinter as tk
from tkinter import messagebox

class GUIManager:
    def __init__(self, game):
        """
        Initialize the GUIManager class
        
        Args:
            game = An instance of the game class that will handle the game logic"
        """
        self.game = game
        self.window = tk.Tk()
        self.window.title("SOS Game")
        self.grid_buttons = []
        self.current_player = None
        self.status_label = None
        self.selected_letter = None 
        self.setup_gui()
    
    def setup_gui(self):
        """
        Setup the GUI layout and components.
        """
        # Header
        self.current_player = tk.Label(self.window, text="Current Player: " + self.game.current_player, font=("Arial", 12))
        self.current_player.grid(row=0, column=0, columnspan=3)

        # Letter Selection Buttons
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=1, column=0, columnspan=3)
        tk.Button(button_frame, text="S", command=lambda: self.select_letter("S")).grid(row=0, column=0)
        tk.Button(button_frame, text="O", command=lambda: self.select_letter("O")).grid(row=0, column=1)

        # Game Board
        board_frame = tk.Frame(self.window)
        board_frame.grid(row=2, column=0, columnspan=3)
        self.create_board(board_frame)
    
    def create_board(self, parent):
        """
        Create the game board as a grid of buttons.
        Args:
            parent: The parent Tkinter widget will contain the board.
        """
        size = self.game.board.size
        for row in range(size):
            button_row = []
            for col in range(size):
                button = tk.Button(
                    parent, 
                    text=" ", 
                    width=5, 
                    height=2, 
                    command=lambda r=row, c=col: self.handle_button_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.grid_buttons.append(button_row)

    
    def select_letter(self, letter):
        """
        Handle letter selection (S or O)

        Args:
            letter: The selected letter (S or O)
        """
        self.selected_letter = letter
    
    def handle_button_click(self, row, col):
        """
        Handle the button click on the game board
        """
        if self.selected_letter is None:
            messagebox.showerror("Error", "Please select a letter first.")
            return
        if self.game.board.grid[row][col] == " ":
            self.game.place_letter(row, col, self.selected_letter)
            self.grid_buttons[row][col].config(text=self.selected_letter)
            self.update_turn()
        else:
            messagebox.showerror("Error", "This square is already taken!")

    def update_turn(self):
        """
        Update GUI to show the current turn and game state
        """
        current_player = self.game.current_player
        self.current_player.config(text="Current Player: " + current_player)
        if self.game.is_game_over():
            winner = self.game.get_winner()
            self.status_label.config(text=f"{winner} wins!" if winner else "It's a tie!")
            for row in self.grid_buttons:
                for button in row:
                    button.config(state=tk.DISABLED)
        else:
            self.selected_letter = None

    def restart_game(self):
        """
        Restart the game by resetting the board and GUI components.
        """
        self.game.restart()
        for row in range(len(self.grid_buttons)):
            for col in range(len(self.grid_buttons[row])):
                self.grid_buttons[row][col].config(text=" ", state=tk.NORMAL)
            self.status_label.config(text="Game in progress")
            self.update_turn()

    def play(self):
        """
        Start the GUI main loop
        """
        self.window.mainloop()