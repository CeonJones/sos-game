import unittest
from sos_game_state import SOSGame

class TestSOSGame(unittest.TestCase):

    def test_sos_win_horizontal_simple(self):
        game = SOSGame(3, mode="Simple Game")
        game.place_letter(0, 0, "S")
        game.place_letter(1, 0, "S")  # Red turn
        game.place_letter(0, 1, "O")
        game.place_letter(1, 1, "O")  # Red turn
        game.place_letter(0, 2, "S")  # Blue forms SOS

        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, "Blue")

    def test_no_win_simple(self):
        game = SOSGame(3, mode="Simple Game")
        game.place_letter(0, 0, "S")
        game.place_letter(0, 1, "S")
        game.place_letter(0, 2, "S")

        self.assertFalse(game.game_over)

    def test_draw_simple(self):
        game = SOSGame(3, mode="Simple Game")
        moves = [
            (0, 0, "S"), (0, 1, "S"), (0, 2, "O"),
            (1, 0, "O"), (1, 1, "O"), (1, 2, "S"),
            (2, 0, "S"), (2, 1, "S"), (2, 2, "O"),
        ]
        for row, col, letter in moves:
            game.place_letter(row, col, letter)

        self.assertTrue(game.game_over)
        self.assertIsNone(game.winner)

    def test_sos_score_horizontal_general(self):
        game = SOSGame(3, mode="General Game")
        game.place_letter(0, 0, "S")
        game.place_letter(1, 0, "S")  # Red
        game.place_letter(0, 1, "O")
        game.place_letter(1, 1, "O")  # Red
        game.place_letter(0, 2, "S")  # Blue forms SOS

        self.assertEqual(game.score["Blue"], 1)
        self.assertFalse(game.game_over)

    def test_sos_score_multiple_general(self):
        game = SOSGame(5, mode="General Game")
        # Create two horizontal SOS for Blue
        game.place_letter(0, 0, "S")
        game.place_letter(1, 0, "S")  # Red
        game.place_letter(0, 1, "O")
        game.place_letter(1, 1, "O")  # Red
        game.place_letter(0, 2, "S")  # Blue scores 1
        game.place_letter(2, 2, "S")  # Red
        game.place_letter(0, 3, "O")
        game.place_letter(2, 3, "O")  # Red
        game.place_letter(0, 4, "S")  # Blue scores again

        self.assertEqual(game.score["Blue"], 2)
        self.assertFalse(game.game_over)

    def test_game_over_on_full_board_general(self):
        game = SOSGame(3, mode="General Game")
        moves = [
            (0, 0, "S"), (0, 1, "O"), (0, 2, "S"),
            (1, 0, "O"), (1, 1, "S"), (1, 2, "O"),
            (2, 0, "S"), (2, 1, "O"), (2, 2, "S"),
        ]
        for row, col, letter in moves:
            game.place_letter(row, col, letter)

        self.assertTrue(game.game_over)
        self.assertIn(game.winner, ["Blue", "Red", None])  # Could be a draw or winner based on SOS found

if __name__ == "__main__":
    unittest.main()