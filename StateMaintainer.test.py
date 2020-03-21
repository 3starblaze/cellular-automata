import unittest

from StateMaintainer import StateMaintainer


def GAME_OF_LIFE_RULESET(cell, values):
    if cell:
        return values.sum() >= 2 and values.sum() <= 3
    else:
        return values.sum() == 3


# One of the valid rules
GAME_OF_LIFE = {
    'indices': [(-1, 1),  (0, 1),  (1, 1),
                (-1, 0),           (1, 0),
                (-1, -1), (0, -1), (1, -1),],
    'ruleset': GAME_OF_LIFE_RULESET
}

VALID_DATA = [[False, False, True],
              [False, True, False],
              [True, False, False]]


class TestStateMaintainer(unittest.TestCase):
    # 'data' argument tests
    def test_incorrectly_shaped_1d_input(self):
        self.assertRaises(ValueError, StateMaintainer,
                          [False, False, True, False, True, True],
                          GAME_OF_LIFE)


    def test_correctly_shaped_2d_input(self):
        try:
            StateMaintainer([[True, False, False],
                             [False, True, False],
                             [False, False, True]],
                            GAME_OF_LIFE)
        except ValueError:
            self.fail("Correctly shapped array raises an exception!")


    def test_incorrectly_shaped_3d_input(self):
        self.assertRaises(ValueError, StateMaintainer,
                          [[[False, False]], [[True, False]], [[True, True]]],
                          GAME_OF_LIFE)


    # 'rules' argument tests
    def test_correct_rule(self):
        try:
            StateMaintainer(VALID_DATA, GAME_OF_LIFE)
        except ValueError:
            self.fail("Correct rule raises an exception!")


    def test_empty_rule(self):
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, {})


if __name__ == '__main__':
    unittest.main()
