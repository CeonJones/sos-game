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
        self.setup_gui()
    
    def setup_gui(self):
        """
        Setup the GUI layout and components.
        """
        # Header
        self.current_player = tk.Label(self.window, text="Current Player: " + self.game.current_player, font=("Arial", 12))
        self.current_player.grid(row=0, column=0, columnspan=3)

        # Frames for player sections
        player_frame = tk.Frame(self.window)
        player_frame.grid(row=0, column=3)

        # Blue Player Frame
        blue_player_frame = tk.LabelFrame(player_frame, text="Blue Player")
        blue_player_frame.grid(row=0, column=0)
        self.create_player_section(blue_player_frame, "Blue")

        # Red Player Frame
        red_player_frame = tk.LabelFrame(player_frame, text="Red Player")
        red_player_frame.grid(row=0, column=1)
        self.create_player_section(red_player_frame, "Red")

        # Game Board
        board_frame = tk.Frame(self.window)
        board_frame.grid(row=2, column=0, columnspan=3)
        self.create_board(board_frame)

        # Status Label
        self.status_label = tk.Label(self.window, text="Game in progress")
        self.status_label.grid(row=3, column=0, columnspan=3)

        # Restart Button
        restart_button = tk.Button(self.window, text="Restart", command=self.restart_game)
        restart_button.grid(row=4, column=0, columnspan=3)

    def create_player_section(self, parent, player_color):
        """
        Create a player section with buttons for selecting a letter and type of player options/
        
        Args:
            parent: The parent Tkinter widget that will contain the player section.
            player_color: The player name (Blue or Red)
        """
        # Variable to store the selected letter
        if player_color == "Blue":
            self.blue_letter = tk.StringVar(value="S")
            self.blue_type = tk.StringVar(value="Human")
        else:
            self.red_letter = tk.StringVar(value="S")
            self.red_type = tk.StringVar(value="Human")
            

        # Letter Selection
        letter_label = tk.Label(parent, text="Select Letter:")
        radio_s = tk.Radiobutton(parent, text="S", variable=self.blue_letter if player_color == "Blue" else self.red_letter, value="S")
        radio_o = tk.Radiobutton(parent, text="O", variable=self.blue_letter if player_color == "Blue" else self.red_letter, value="O")
        letter_label.grid(row=0, column=0)
        radio_s.grid(row=0, column=1)
        radio_o.grid(row=0, column=2)

        # Player Type Selection
        type_label = tk.Label(parent, text="Select Type:")
        radio_human = tk.Radiobutton(parent, text="Human", variable=self.blue_type if player_color == "Blue" else self.red_type, value="Human")
        radio_cpu = tk.Radiobutton(parent, text="CPU", variable=self.blue_type if player_color == "Blue" else self.red_type, value="CPU")

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

                # Debugging: check the button storage
                print(f" storing button at ({row}, {col}) -> {button}")

            self.grid_buttons.append(button_row)

        # Debugging: check the final button storage
        print(f"Final button storage: {self.grid_buttons}")
    
    def handle_button_click(self, row, col):
        """
        Handle the button click on the game board

        Args:
            row: The row index of the clicked button
            col: The column index of the clicked button
        """
        # Find the current player's selected letter
        selected_letter = self.blue_letter.get() if self.game.current_player == "Blue" else self.red_letter.get()

        # Place the letter if the square is taken
        if self.game.board.grid[row][col] == " ":
             self.game.place_letter(row, col, selected_letter)

             # Debugging: check the placement position of the letter
             print(f"Placing letter {selected_letter} at ({row}, {col})")

             # Debugging: check the storage position before update
             print(f" Before update: Button at ({row}, {col}) text: {self.grid_buttons[row][col]['text']}")
            
            # Update the button text
             self.grid_buttons[row][col].config(text=selected_letter)

            #  Debugging: check the storage position after update
             print(f" After update: Button at ({row}, {col}) text: {self.grid_buttons[row][col]['text']}")

            # Update player turn 
             self.update_turn()
        else:
            messagebox.showerror("Error", "This square is already taken!")

    def update_turn(self):
        """
        Update GUI to show the current turn and game state
        """
        current_player = self.game.current_player
        self.current_player.config(text="Current Player: " + current_player)

        # Check if it's a CPU player
        if (current_player == "Blue" and self.blue_type.get() == "CPU") or (current_player == "Red" and self.red_type.get() == "CPU"):
            self.make_cpu_move()

    #def make_cpu_move(self):
        """
        Make a move for the CPU player
        """
        #is_cpu_turn = (self.game.current_player == "Blue" and self.blue_type.get() == "CPU") or (self.game.current_player == "Red" and self.red_type.get() == "CPU")
        #if not is_cpu_turn:
            #return

        # CPU logic: Place letter in first open spot
        #for row in range(self.game.board.size):
            #for col in range(self.game.board.size):
                #if self.game.board.grid[row][col] == " ":
                    #selected_letter = self.blue_letter.get() if self.game.current_player == "Blue" else self.red_letter.get()
                    #self.game.place_letter(row, col, selected_letter)
                    #self.grid_buttons[row][col].config(text=selected_letter)
                    #self.update_turn()
                    #return

    def restart_game(self):
        """
        Restart the game by resetting the board and GUI components.
        """
        self.game.reset()
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