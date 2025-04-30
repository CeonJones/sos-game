import subprocess
import json
import re
import abc
import math
import os
import io
import contextlib
import random
from config import SIMPLE_MODE, GENERAL_MODE, ALLOWED_LETTERS
from sos_game_state import SOSGame

class ComputerPlayer(abc.ABC):
    """
    Interface for all type of CPU players
    """
    @abc.abstractmethod
    def choose_move(self, game: SOSGame):
        """
        Return dict {'row': int, 'col': int, 'letter': 'S' or 'O'}
        Gets live SOSgame instance
        """
        pass

class Simulation:
    """
    Wrapper for SOSGame that lets us apply and undo moves in O(1), so minimax
    can explore
    """
    def __init__(self, sos_game: SOSGame):
        self.size = sos_game.board.size
        self.board = [row[:] for row in sos_game.board.grid]
        self.owner_grid = [row[:] for row in sos_game.owner_grid]
        self.mode = sos_game.mode
        self.current_player = sos_game.current_player
        self.score = dict(sos_game.score) if sos_game.score is not None else None
        #self.move_counter = sos_game.move_counter if self.mode == GENERAL_MODE else None
        self.move_counter = None
        self.scored_moves = set(sos_game.scored_moves) if self.mode == GENERAL_MODE else None
        self.game_over = sos_game.game_over
        self.winner = sos_game.winner

        # Undo stack
        self._stack = []

    def legal_moves(self):
        """
        All (row ,col, letter) triples on empty cells
        """
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == " ":
                    for letter in ["S", "O"]:
                        moves.append((r, c, letter))
        return moves

    def apply_move(self, move):
        r, c, letter = move

        #save the game state onto the undo stack
        snapshot = {
            'cell': (r, c, self.board[r][c]),
            'score': dict(self.score) if self.score is not None else None,
            'current_player': self.current_player,
            #'move_counter': self.move_counter,
            'scored_moves': set(self.scored_moves) if self.scored_moves is not None else None,
            'game_over': self.game_over,
            'winner': self.winner,
        }
        self._stack.append(snapshot)

        # place letter
        self.board[r][c] = letter
        self.owner_grid[r][c] = self.current_player
        #if self.mode == GENERAL_MODE:
        #    self.move_counter += 1

        # scoring, win/draw logic for temporary simulation
        temp = SOSGame(self.size, self.mode)
        temp.board.grid = [row[:] for row in self.board]
        temp.owner_grid = [row[:] for row in self.owner_grid]
        if temp.score is not None:
            temp.score = dict(self.score)
            #temp.move_counter = self.move_counter
            temp.scored_moves = set(self.scored_moves)
        temp.current_player = self.current_player
        temp.game_over = self.game_over
        temp.winner = self.winner

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sos_found = temp.check_sos_after_move(self.current_player, r, c, letter)

        # pull back updated scoring and flags
        if self.score is not None:
            self.score = dict(temp.score)
            #self.move_counter = temp.move_counter
            self.scored_moves = set(temp.scored_moves)
        self.game_over = temp.game_over
        self.winner = temp.winner

        # swtich the current player
        if self.mode == GENERAL_MODE:
            if not sos_found and not self.game_over:
                self.current_player = "Red" if self.current_player == "Blue" else "Blue"
        # simple mode
        else:
            if not sos_found and not self.game_over:
                self.current_player = "Red" if self.current_player == "Blue" else "Blue"

        # end of game detection
        full = all(self.board[r][c] != " "
                   for r in range(self.size) for c in range(self.size))
        if full and not self.game_over:
            self.game_over = True
            if self.mode == GENERAL_MODE:
                # compare scores
                b, R = self.score["Blue"], self.score["Red"]
                if b > R:
                    self.winner = "Blue"
                elif R > b:
                    self.winner = "Red"
                else:
                    self.winner = None
            else:
                # draw in simple game
                self.winner = None

    def undo_move(self, move):
        """
        Restore the previous game state
        """
        snapshot = self._stack.pop()
        r, c, old = snapshot['cell']
        self.board[r][c] = old
        if snapshot['score'] is not None:
            self.score = dict(snapshot['score'])
            #self.move_counter = snapshot['move_counter']
            self.scored_moves = set(snapshot['scored_moves'])
        self.current_player = snapshot['current_player']
        self.game_over = snapshot['game_over']
        self.winner = snapshot['winner']

class MinimaxPlayer(ComputerPlayer):
    """
    Minimax player with alpha-beta pruning that looks ahead up to the
    specified depth.
    """
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

    def choose_move(self, game: SOSGame):
        root = game.current_player
        for r, c, letter in Simulation(game).legal_moves():
            sim = Simulation(game)
            sim.apply_move((r, c, letter))
            if sim.score and sim.score[root] > game.score[root]:
                return {"row": r, "col": c, "letter": letter}
        # remember the root node
        self._root = game.current_player
        sim = Simulation(game)

        move, _ = self._minimax(
            sim,
            depth=self.max_depth,
            alpha=-math.inf,
            beta=math.inf,
            maximizing=True
        )
        # if no move is found, return a random legal move
        if move is None:
            legal = sim.legal_moves()
            if not legal:
                return None
            move = random.choice(legal)
        r, c, letter = move
        return {"row": r, "col": c, "letter": letter}
    
    def _evaluate(self, sim: Simulation):
        if sim.game_over:
            if sim.winner == self._root: return math.inf
            if sim.winner is None: return 0
            return -math.inf
        
        if sim.score is not None:
            opponent = "Red" if self._root == "Blue" else "Blue"
            base = sim.score[self._root] - sim.score[opponent]
            return base + 0.1 * (self._count_threats(sim, self._root) - self._count_threats(sim, opponent))
            #return sim.score[self._root] - sim.score[opponent]
        return 0
    
    def _count_threats(self, sim: Simulation, player: str) -> int:
        threats = 0
        dirs = [(0,1), (1,0), (1,1), (1,-1)]
        for r in range(sim.size):
            for c in range(sim.size):
                for dr, dc in dirs:
                     r2, c2 = r+2*dr, c+2*dc
                     rm, cm = r+dr, c+dc
                     if (0 <= r2 < sim.size and 0 <= c2 < sim.size and
                        sim.board[r][c]=="S" and
                        sim.board[r2][c2]=="S" and
                        sim.board[rm][cm]==" "):
                        # only count it if those ‘S’ were owned by that player
                        if (sim.owner_grid[r][c]==player and
                            sim.owner_grid[r2][c2]==player):
                            threats += 1
        return threats
    
    def _minimax(self, sim, depth, alpha, beta, maximizing):
        if sim.game_over or depth == 0:
            return None, self._evaluate(sim)
        
        best_move = None
        if maximizing:
            value = -math.inf
            for move in sim.legal_moves():
                sim.apply_move(move)
                _, score = self._minimax(sim, depth-1, False, alpha, beta)
                sim.undo_move(move)

                if score > value:
                    value, best_move = score, move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_move, value
        
        # minimizing
        value = math.inf
        for move in sim.legal_moves():
            sim.apply_move(move)
            _, score = self._minimax(sim, depth-1, True, alpha, beta)
            sim.undo_move(move)

            if score < value:
                value, best_move = score, move
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_move, value