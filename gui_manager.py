import tkinter as tk
from tkinter import messagebox
from sos_game_state import SOSGame

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
        #self.setup_gui()

        self.game = None

        self.setup_game_mode()

    def setup_game_mode(self):
        """
        Setup game mode ui 
        """
        self.board_size_input = tk.Entry(self.window)
        self.board_size_input.insert(0, "Enter board size (3-10):")
        self.board_size_input.grid(row=0, column=0, columnspan=3)

        # Game mode select
        self.game_mode = tk.StringVar(value="Simple Game")
        tk.Radiobutton(self.window, text="Simple Game", variable=self.game_mode, value="Simple Game").grid(row=1, column=0)
        tk.Radiobutton(self.window, text="General Game", variable=self.game_mode, value="General Game").grid(row=1, column=1)
        tk.Button(self.window, text="Start Game", command=self.begin_game).grid(row=1, column=2)

    def begin_game(self):
        try:
            size = int(self.board_size_input.get())
            selected_mode = self.game_mode.get()
            self.game = SOSGame(size, selected_mode)

            for widget in self.window.winfo_children():
                widget.destroy()
            self.setup_gui()
        except ValueError:
            messagebox.showerror("Error", "Board size must be between 3 and 10")
    
    def setup_gui(self):
        """
        Setup the GUI layout and components.
        """

        # Header
        self.current_player = tk.Label(self.window, text="Current Player: " + self.game.current_player, font=("Arial", 12))
        self.current_player.grid(row=0, column=0, columnspan=3)

        # Board Size Input
        #self.board_size_input = tk.Entry(self.window)
        #self.board_size_input.grid(row=2, column=3, columnspan=3)
        #self.board_size_input.insert(0, int(self.game.board.size))

        # Board Size button
        #board_size_button = tk.Button(self.window, text="Enter Board Size", command=self.change_board_size)
        #board_size_button.grid(row=2, column=4, columnspan=3)

        # Game mode select
        #self.game_mode = tk.StringVar(value="Simple Game")
        #game_mode_label = tk.Label(self.window, text="Pick a Game Mode:")
        #game_mode_label.grid(row=3, column=3)

        #simple_game_button = tk.Radiobutton(self.window, text="Simple Game", variable=self.game_mode, value="Simple Game")
        #general_game_button = tk.Radiobutton(self.window, text="General Game", variable=self.game_mode, value="General Game")

        #simple_game_button.grid(row=3, column=4)
        #general_game_button.grid(row=3, column=5)

        # Create game board after GUI is setup
        self.create_board(self.window)

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

        # General Game tally
        self.blue_score_label = tk.Label(self.window, text="Blue Score: 0")
        self.red_score_label = tk.Label(self.window, text="Red Score: 0")
        self.blue_score_label.grid(row=5, column=0)
        self.red_score_label.grid(row=5, column=1)


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
        letter_label.grid(row=0, column=0)


        if player_color == "Blue":
            self.radio_s_blue = tk.Radiobutton(parent, text="S", variable=self.blue_letter, value="S")
            self.radio_o_blue = tk.Radiobutton(parent, text="O", variable=self.blue_letter, value="O")
            self.radio_human_blue = tk.Radiobutton(parent, text="Human", variable=self.blue_type, value="Human")
            self.radio_cpu_blue = tk.Radiobutton(parent, text="CPU", variable=self.blue_type, value="CPU")
            self.radio_s_blue.grid(row=0, column=1)
            self.radio_o_blue.grid(row=0, column=2)

        else:
            self.radio_s_red = tk.Radiobutton(parent, text="S", variable=self.red_letter, value="S")
            self.radio_o_red = tk.Radiobutton(parent, text="O", variable=self.red_letter, value="O")
            self.radio_human_red = tk.Radiobutton(parent, text="Human", variable=self.red_type, value="Human")
            self.radio_cpu_red = tk.Radiobutton(parent, text="CPU", variable=self.red_type, value="CPU")
            self.radio_s_red.grid(row=0, column=1)
            self.radio_o_red.grid(row=0, column=2)
        

        # Player Type Selection
        type_label = tk.Label(parent, text="Select Type:")
        radio_human = tk.Radiobutton(parent, text="Human", variable=self.blue_type if player_color == "Blue" else self.red_type, value="Human")
        radio_cpu = tk.Radiobutton(parent, text="CPU", variable=self.blue_type if player_color == "Blue" else self.red_type, value="CPU")
    
    def change_board_size(self):
        """
        Change size of the game board based on the user's input

        Args:
            parent: The parent Tkinter widget that will contain the board.
        """
        try:     
            size = int(self.board_size_input.get())
            if size < 3 or size > 10:
                raise ValueError("Error: ", "Board size must be between 3 and 10")
            selected_mode = self.game_mode.get()
            self.window.destroy()
            self.window = tk.Tk()
            self.window.title("SOS Game")
            
            self.game = SOSGame(size, selected_mode)
            print(f"Game mode: {self.game.mode}")
            
            # Restart a game with new board size
            #self.window.destroy()
            
            # Make new window instance after destroying old one
            #self.window = tk.Tk()
            #self.window.title("SOS Game")

            # New game with new board size
            #self.game = SOSGame(size, mode)
            
            # Reset GUI
            self.grid_buttons = []
            self.current_player = None
            self.status_label = None 
            self.setup_gui()

            if self.game.mode == "General Game":
                self.blue_score_label.config(text="Blue Score: 0")
                self.red_score_label.config(text="Red Score: 0")
            else:
                self.blue_score_label.config(text="Blue Score: 0")
                self.red_score_label.config(text="Red Score: 0")
            #self.create_board()
        
        except ValueError:
            messagebox.showerror("Error", "Board size must be between 3 and 10")



    def create_board(self, parent):
        """
        Create the game board as a grid of buttons.
        Args:
            parent: The parent Tkinter widget will contain the board.
        """
        size = self.game.board.size

        # Remove old buttons
        if self.grid_buttons:
            for row in self.grid_buttons:
                for button in row:
                    button.destroy()
        
        self.grid_buttons = []

        board_frame = tk.Frame(self.window)
        board_frame.grid(row=1, column=0, columnspan=size)

        for row in range(size):
            button_row = []
            for col in range(size):
                button = tk.Button(
                    board_frame, 
                    text=" ", 
                    width=5, 
                    height=2, 
                    command=lambda r=row, c=col: self.handle_button_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)

                # Debugging: check the button storage
                #print(f" storing button at ({row}, {col}) -> {button}")

            self.grid_buttons.append(button_row)

        # Debugging: check the final button storage
        #print(f"Final button storage: {self.grid_buttons}")
    
    def handle_button_click(self, row, col):
        """
        Handle the button click on the game board

        Args:
            row: The row index of the clicked button
            col: The column index of the clicked button
        """
        # Find the current player's selected letter
        selected_letter = self.blue_letter.get() if self.game.current_player == "Blue" else self.red_letter.get()

        # Place the letter if the square is not taken
        if self.game.board.grid[row][col] == " ":
             #self.game.place_letter(row, col, selected_letter)

             player = self.game.current_player
             self.game.place_letter(row, col, selected_letter)
            
            # Update the button text
             self.grid_buttons[row][col].config(text=selected_letter)

             # Check of SOS after move
             if self.game.mode == "General Game":
                 blue_score = self.game.score["Blue"]
                 red_score = self.game.score["Red"]
                 self.blue_score_label.config(text=f"Blue Score: {blue_score}")
                 self.red_score_label.config(text=f"Red Score: {red_score}")

             if not self.game.game_over:
                 self.update_turn()

             if self.game.game_over:
                 if self.game.winner:
                        self.status_label.config(text=f"{self.game.winner} wins!")
                 else:
                        self.status_label.config(text="It's a draw!")
                 return
                 
             #if self.game.check_sos_after_move(player, row, col):
                 #if self.game.mode == "General Game":
                     #blue_score = self.game.score["Blue"]
                     #red_score = self.game.score["Red"]
                     #self.blue_score_label.config(text=f"Blue Score: {blue_score}")
                     #self.red_score_label.config(text=f"Red Score: {red_score}")
                 #print(f"SOS found after move at: ({row}, {col})")
             
             # Check if the game is over
             if self.game.game_over:
                 if self.game.winner:
                     self.status_label.config(text=f"{self.game.winner} wins!")
                 else:
                     self.status_label.config(text="It's a draw!")
            # Debugging: check the storage position after update
             #print(f" After update: Button at ({row}, {col}) text: {self.grid_buttons[row][col]['text']}")
                 

            # Update player turn 
             #self.update_turn()

             
        else:
            messagebox.showerror("Error", "This square is already taken!")

             # Check for SOS after the move
            #if self.game.check_sos_after_move():
                #self.status_label.config(text=f"{self.game.current_player} wins!")

    def update_turn(self):
        """
        Update GUI to show the current turn and game state
        """
        current_player = self.game.current_player
        self.current_player.config(text="Current Player: " + current_player)

        # Enable active players radio buttons, disable inactive player radio button based on whose turn it is
        blue_control = [self.radio_s_blue, self.radio_o_blue, self.radio_human_blue, self.radio_cpu_blue]
        red_control = [self.radio_s_red, self.radio_o_red, self.radio_human_red, self.radio_cpu_red]

        # Disable/Enable radio buttons based on current players turn
        if current_player == "Blue":
            # disable red player buttons, enable blue player buttons
            for widget in blue_control:
                widget.config(state=tk.NORMAL)
            for widget in red_control:
                widget.config(state=tk.DISABLED)
        else:
            # disable blue player buttons, enable red player buttons 
            for widget in blue_control:
                widget.config(state=tk.DISABLED)
            for widget in red_control:
                widget.config(state=tk.NORMAL)


        # Check if it's a CPU player
        if (current_player == "Blue" and self.blue_type.get() == "CPU") or (current_player == "Red" and self.red_type.get() == "CPU"):
            self.make_cpu_move()

    #def make_cpu_move(self):
        """
        Make a move for the CPU player

        No functionality is added here, simply placeholder for logic to be added later
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
        if not self.game:
            messagebox.showerror("Error", "Game not started yet!")
            return
        self.game.reset()
        if self.game.mode == "General Game":
            self.blue_score_label.config(text="Blue Score: 0")
            self.red_score_label.config(text="Red Score: 0")
        else:
            self.blue_score_label.config(text="Blue Score: 0")
            self.red_score_label.config(text="Red Score: 0")
        
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