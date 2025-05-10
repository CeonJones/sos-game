import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from sos_game_state import SOSGame
from computer_player import ComputerPlayer, MinimaxPlayer

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Please set the OPENAI_API_KEY environment variable.")
client = OpenAI(api_key=OPENAI_API_KEY)


class LLMPlayer(ComputerPlayer):
    def __init__(self, model="gpt-4", max_depth=3):
        self.model = model
        self.max_depth = max_depth

    def choose_move(self, game: SOSGame):
        board = "\n".join("".join(row) for row in game.board.grid)
        legal = set(game.get_state_game()["legal_moves"])
        prompt = (
            f"You are playing SOS on a {game.board.size}×{game.board.size} board.\n"
            f"Current player is: {game.current_player}\n"
            f"Board:\n{board}\n\n"
            "Return your move as JSON {\"row\":int, \"col\":int, \"letter\":\"S\" or \"O\"}.\n"
            "Pick the move that gives you the best chance of making SOS immediately or setting one up."
        )
        try: 
            response = client.chat.completions.create(
                model = self.model,
                messages = [
                    {"role": "system", "content": "You are a game-playing AI that plays the game SOS."},
                    {"role": "user", "content": prompt}],
                temperature = 0.7
            )
            text = response.choices[0].message.content.strip()
            move = json.loads(text)
            
            r, c, letter = move["row"], move["col"], move["letter"]
            if (r, c) in legal and letter in {"S", "O"}:
                return {"row": r, "col": c, "letter": letter}
            else:
                raise ValueError(f"LLM suggested illegal move {move}")
        except Exception as e:
            print(f"Error in LLM response: {e}")
            return MinimaxPlayer(max_depth=self.max_depth).choose_move(game)
        
                