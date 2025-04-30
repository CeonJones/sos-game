import tkinter as tk
from tkinter import messagebox
from sos_game_state import SOSGame
from computer_player import MinimaxPlayer
import random

class GUIManager:
    def __init__(self):
        """
        Initialize the GUIManager class.
        Instance of the game will be created from the startup screen.
        """
        self.game = None
        self.window = tk.Tk()
        self.window.title("SOS Game")
        self.current_player_label = None
        self.status_label = None
        self.blue_score_label = None
        self.red_score_label = None 

        # Computer player instances (if needed)
        self.blue_cpu_player = None
        self.red_cpu_player = None
        
        self.init_startup_screen()

    def init_startup_screen(self):
        """
        Create a strartup screen to input the board size and game mode.
        """
        self.startup_frame = tk.Frame(self.window)
        self.startup_frame.pack(padx=10, pady=10)

        # Board size
        label = tk.Label(self.startup_frame, text="Enter board size (3-10):")
        label.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.board_size_input = tk.Entry(self.startup_frame)
        self.board_size_input.grid(row=1, column=0, columnspan=2, pady=5)

        # Game mode
        self.game_mode = tk.StringVar(value="Simple Game")
        rdio1 = tk.Radiobutton(self.startup_frame, text="Simple Game", variable = self.game_mode, value="Simple Game")
        rdio1.grid(row=2, column=0, pady=5, sticky="w")
        rdio2 = tk.Radiobutton(self.startup_frame, text="General Game", variable = self.game_mode, value="General Game")
        rdio2.grid(row=2, column=1, pady=5, sticky="w")

        # Who starts first
        tk.Label(self.startup_frame, text="Who starts first?").grid(row=3, column=0, sticky="nsew")
        self.first_player = tk.StringVar(value="Blue")
        tk.Radiobutton(self.startup_frame, text="Blue", variable=self.first_player, value="Blue")\
            .grid(row=4, column=0, sticky="w")
        tk.Radiobutton(self.startup_frame, text="Red", variable=self.first_player, value="Red")\
            .grid(row=4, column=1, sticky="w")
        tk.Radiobutton(self.startup_frame, text="Random", variable=self.first_player, value="Random")\
            .grid(row=4, column=2, sticky="w")
        
        # Player types
        tk.Label(self.startup_frame, text="Blue Player Type:").grid(row=5, column=0, sticky="w")
        self.startup_blue_type = tk.StringVar(value="Human")
        tk.Radiobutton(self.startup_frame, text="Human", variable=self.startup_blue_type, value="Human")\
            .grid(row=6, column=0, sticky="w")
        tk.Radiobutton(self.startup_frame, text="CPU", variable=self.startup_blue_type, value="CPU")\
            .grid(row=6, column=1, sticky="w")
        tk.Label(self.startup_frame, text="Red Player Type:").grid(row=7, column=0, sticky="w")
        self.startup_red_type = tk.StringVar(value="Human")
        tk.Radiobutton(self.startup_frame, text="Human", variable=self.startup_red_type, value="Human")\
            .grid(row=8, column=0, sticky="w")
        tk.Radiobutton(self.startup_frame, text="CPU", variable=self.startup_red_type, value="CPU")\
            .grid(row=8, column=1, sticky="w")
        
        # Start button
        start_button = tk.Button(self.startup_frame, text="Start Game", command=self.begin_game)
        start_button.grid(row=9, column=0, columnspan=3, pady=10)

    def begin_game(self):
        """
        Make a new game instance using board size and game mode input from startup screen,
        then destroy the startup screen and initilize the game GUI.
        """
        try:
            size = int(self.board_size_input.get())
            selected_mode = self.game_mode.get()
            self.game = SOSGame(size, selected_mode)
        except ValueError:
            messagebox.showerror("Error", "Board size must be between 3 and 10")
            return
        
        # Set the first player
        starter = self.first_player.get()
        if starter == "Red":
            self.game.current_player = "Red"
        elif starter == "Random":
            self.game.current_player = random.choice(["Red", "Blue"])
        
        # Remove startup screen and load the main game UI
        self.startup_frame.destroy()
        self.setup_main_ui()

        # Setup player types
        self.blue_type.set(self.startup_blue_type.get())
        self.red_type.set(self.startup_red_type.get())

        # Setup computer players (SingleShotPlayer implementation).
        # They use defualt LLM interface, which can be customized via environment variables
        #llm_interface = LLMInterface()
        self.blue_cpu_player = MinimaxPlayer(max_depth=3)
        self.red_cpu_player = MinimaxPlayer(max_depth=3)

        # Update the turn label
        self.update_turn()
    
    def setup_main_ui(self):
        """
        Set up main game UI after startup screen is destroyed.
        The UI has current player, game board, controls, status, score for general game,
        and restart button 
        """
        # Current player label
        self.current_player_label = tk.Label(self.window, text="Current Player: " + self.game.current_player, font=("Helvetica", 12))
        self.current_player_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Make game board
        self.create_board()

        # Create player controls
        player_frame = tk.Frame(self.window)
        player_frame.grid(row=0, column=3, padx=10, pady=5, sticky="nsew")

        # Blue player panel
        blue_panel = tk.LabelFrame(player_frame, text="Blue Player")
        blue_panel.grid(row=0, column=0, padx=5)
        self.create_player_section(blue_panel, "Blue")

        # Red player panel
        red_panel = tk.LabelFrame(player_frame, text="Red Player")
        red_panel.grid(row=0, column=1, padx=5)
        self.create_player_section(red_panel, "Red")

        # Game status message label
        self.status_label = tk.Label(self.window, text="Game in progress")
        self.status_label.grid(row=3, column=0, columnspan=3, pady=5)

        # Score labels (General Game mode)
        if self.game.mode == "General Game":
            self.blue_score_label = tk.Label(self.window, text="Blue Score: 0")
            self.blue_score_label.grid(row=4, column=0, pady=5)
            self.red_score_label = tk.Label(self.window, text="Red Score: 0")
            self.red_score_label.grid(row=4, column=1, pady=5)
        
        # Restart button
        restart_button = tk.Button(self.window, text="Restart", command=self.restart_game)
        restart_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Back button to go back to the start screen
        back_button = tk.Button(self.window, text="Back", command=self.back_to_start)
        back_button.grid(row=6, column=0, columnspan=3, pady=10)

    def create_board(self):
        """
        Create game board as grid of buttons
        """
        size = self.game.board.size
        self.board_frame = tk.Frame(self.window)
        self.board_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # Define cell dimensions
        self.cell_width = 50
        self.cell_height = 50
        canvas_width = self.cell_width * size
        canvas_height = self.cell_height * size

        # Create canvas that will contain buttons and drawn SOS lines
        self.canvas = tk.Canvas(self.board_frame, width=canvas_width, height=canvas_height, background="white")
        self.canvas.pack(fill='both', expand=True)
        
        self.cell_rect_ids = {}
        self.cell_text_ids = {}
        
        for r in range(size):
            for c in range(size):
                x0 = c * self.cell_width
                y0 = r * self.cell_height
                x1 = x0 + self.cell_width
                y1 = y0 + self.cell_height

                # Draw rectangle for each cell
                rect_id = self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")
                self.cell_rect_ids[(r, c)] = rect_id

                #Draw text cell
                text_id = self.canvas.create_text(x0 + self.cell_width / 2, y0 + self.cell_height / 2, text= "", font=("Helvetica", 16))
                self.cell_text_ids[(r, c)] = text_id

            self.canvas.bind("<Button-1>", self.handle_canvas_click)

    def get_button_center(self, row, col):
        """
        Find the center and return the coordinfates of buttons in the grid using fixed cell measurements.

        Returns:
            tuple: center_x, center_y
        """
        center_x = col * self.cell_width + self.cell_width / 2
        center_y = row * self.cell_height + self.cell_height / 2
        return (center_x, center_y)

    def create_player_section(self, parent, player_color):
        """
        Create a player section with buttons for selecting a letter
        
        Args:
         p   arent: The parent Tkinter widget that will contain the player section.
            player_color: The player name (Blue or Red)
        """
        if player_color == "Blue":
            self.blue_letter = tk.StringVar(value="S")
            self.blue_type = tk.StringVar(value="Human")
            label = tk.Label(parent, text="Select letter:")
            label.grid(row=0, column=0)
            self.radio_s_blue = tk.Radiobutton(parent, text="S", variable=self.blue_letter, value="S")
            self.radio_o_blue = tk.Radiobutton(parent, text="O", variable=self.blue_letter, value="O")
            self.radio_s_blue.grid(row=0, column=1)
            self.radio_o_blue.grid(row=0, column=2)

            # Player type selection
            type_label = tk.Label(parent, text="Player type:")
            type_label.grid(row=1, column=0)
            self.blue_type_human = tk.Radiobutton(parent, text="Human", variable=self.blue_type, value="Human")
            self.blue_type_cpu = tk.Radiobutton(parent, text="CPU", variable=self.blue_type, value="CPU")
            self.blue_type_human.grid(row=1, column=1)
            self.blue_type_cpu.grid(row=1, column=2)
        else:
            self.red_letter = tk.StringVar(value="S")
            self.red_type = tk.StringVar(value="Human")
            label = tk.Label(parent, text="Select letter:")
            label.grid(row=0, column=0)
            self.radio_s_red = tk.Radiobutton(parent, text="S", variable=self.red_letter, value="S")
            self.radio_o_red = tk.Radiobutton(parent, text="O", variable=self.red_letter, value="O")
            self.radio_s_red.grid(row=0, column=1)
            self.radio_o_red.grid(row=0, column=2)
            # Player type seletion
            type_label = tk.Label(parent, text="Player type:")
            type_label.grid(row=1, column=0)
            self.red_type_human = tk.Radiobutton(parent, text="Human", variable=self.red_type, value="Human")
            self.red_type_cpu = tk.Radiobutton(parent, text="CPU", variable=self.red_type, value="CPU")
            self.red_type_human.grid(row=1, column=1)
            self.red_type_cpu.grid(row=1, column=2)

    def update_turn(self):
        """
        Update GUI to show the current turn and game state.
        If active player is set to computer, automatically trigger its move.
        """
        if self.game.game_over:
            return
        self.current_player_label.config(text="Current Player: " + self.game.current_player)

        #Enable and disable letter selcetion based on active player
        if self.game.current_player == "Blue":
            for widget in [self.radio_s_blue, self.radio_o_blue]:
                widget.config(state=tk.NORMAL)
            for widget in [self.radio_s_red, self.radio_o_red]:
                widget.config(state=tk.DISABLED)
            # If blue is a CPU make move after delay
            if self.blue_type.get() == "CPU":
                self.window.after(1000, self.make_cpu_move)
        else:
            for widget in [self.radio_s_blue, self.radio_o_blue]:
                widget.config(state=tk.DISABLED)
            for widget in [self.radio_s_red, self.radio_o_red]:
                widget.config(state=tk.NORMAL)
            if self.red_type.get() == "CPU":
                self.window.after(1000, self.make_cpu_move)


    def make_cpu_move(self):
        """
        Called when player is a CPU.
        Get current game state, calls CPU to move and applies move to update game state and GUI
        """
        if self.game.game_over:
            return
        current_player = self.game.current_player
        player_cpu = self.blue_cpu_player if current_player == "Blue" else self.red_cpu_player
        move = player_cpu.choose_move(self.game)
        if not move:
            return
        
        # Get row, column, and letter from the move
        r , c, letter = move["row"], move["col"], move["letter"]
        if not self.game.place_letter(r, c, letter):
            print("CPU move failed. Using fallback behavior")
            return

        #if self.game.place_letter(r, c, letter):
        self.canvas.itemconfig(self.cell_text_ids[(r, c)], text=letter)
        mover_color = "lightblue" if current_player == "Blue" else "lightcoral"
        self.canvas.itemconfig(self.cell_rect_ids[(r, c)], fill=mover_color)

        if self.game.mode == "General Game":
            self.blue_score_label.config(text=f"Blue Score: {self.game.score['Blue']}")
            self.red_score_label.config(text=f"Red Score: {self.game.score['Red']}")

        if self.game.game_over:
            if self.game.winner:
                self.status_label.config(text=f"{self.game.winner} wins!")
            else:
                self.status_label.config(text="It's a draw!")
            return
        # Update the turn label
        self.update_turn()

    def handle_canvas_click(self, event):
        """
        Handle a click on th ecnavas by getting row and column based on event coordinates t
        swtichting to handle_cell_click
        """
        col = int(event.x // self.cell_width)
        row = int(event.y // self.cell_height)
        self.handle_cell_click(row, col)

    def handle_cell_click(self, row, col):
        """
        Handle clicks on the game board
        Args:
            row: The row index of the clicked cell
            col: The column index of the clicked cell
        """
        active_player = self.game.current_player
        selected_letter = self.blue_letter.get() if active_player == "Blue" else self.red_letter.get()

        if self.game.board.grid[row][col] == " ":
            prev_sequence_count = len(self.game.sos_sequences)

            #Try to place letter and update game state
            if self.game.place_letter(row, col, selected_letter):
                # Update text in cell with a letter
                self.canvas.itemconfig(self.cell_text_ids[(row, col)], text=selected_letter)
                # Change cell backgorund color based on current player
                mover_color = "lightblue" if active_player == "Blue" else "lightcoral"
                self.canvas.itemconfig(self.cell_rect_ids[(row, col)], fill=mover_color)

                # For general game update score labels
                if self.game.mode == "General Game":
                    self.blue_score_label.config(text=f"Blue Score: {self.game.score['Blue']}")
                    self.red_score_label.config(text=f"Red Score: {self.game.score['Red']}")
            
            if self.game.game_over:
                if self.game.winner:
                    self.status_label.config(text=f"{self.game.winner} wins!")
                else:
                    self.status_label.config(text="It's a draw!")
            else:
                self.update_turn()
        else:
            messagebox.showerror("Error", "Square taken!")


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

        for r in range(self.game.board.size):
            for c in range(self.game.board.size):
                self.canvas.itemconfig(self.cell_text_ids[(r, c)], text="")
                self.canvas.itemconfig(self.cell_rect_ids[(r, c)], fill="white")

        self.status_label.config(text="Game in progress")
        self.update_turn()

    def back_to_start(self):
        """
        Handle navigation back to the start screen and destory current instance of the game
        """
        for widget in self.window.winfo_children():
            widget.destroy()
        self.game = None
        self.init_startup_screen()

    def play(self):
        """
        Start the GUI main loop
        """
        self.window.mainloop()

if __name__ == "__main__":
    gui = GUIManager()
    gui.play()