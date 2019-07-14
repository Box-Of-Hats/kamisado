import kamisado
import unittest


class KamisadoTests (unittest.TestCase):
    def test_unconstrained_move(self):
        game = kamisado.Kamisado(8)
        game.gameboard = [[0, 1, 2, 3, 4, 5, 6, 7],
                          [0, 1, 2, 3, 4, 5, 6, 7],
                          ["m", 1, 2, 3, 4, 5, 6, 7],
                          [0, 1, 2, 3, 4, 5, 6, 7],
                          [0, 1, 2, 3, 4, 5, 6, 7],
                          [0, 1, 2, 3, 4, 5, 6, 7],
                          [0, 1, 2, 3, 4, 5, 6, 7],
                          [0, 1, 2, 3, 4, 5, 6, 7]]

        expected_gamestate = [[0, 1, 2, 3, 4, 5, 6, 7],
                              [0, 1, 2, 3, 4, 5, 6, 7],
                              [0, 1, 2, 3, 4, 5, 6, 7],
                              [0, 1, 2, 3, 4, 5, 6, 7],
                              [0, "m", 2, 3, 4, 5, 6, 7],
                              [0, 1, 2, 3, 4, 5, 6, 7],
                              [0, 1, 2, 3, 4, 5, 6, 7],
                              [0, 1, 2, 3, 4, 5, 6, 7]]

        game.move_piece_ignoring_constraints((0, 2), (1, 4))
        self.assertEqual(expected_gamestate, game.gameboard)


if __name__ == "__main__":
    unittest.main()
