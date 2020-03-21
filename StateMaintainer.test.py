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


    def test_rule_with_invalid_keys(self):
        test_rule = {
            'banana': [(4, 2), (1, 2)],
            'carrot': lambda x: x - 1
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)


    def test_rule_with_valid_indices_but_missing_ruleset(self):
        test_rule = {
            'indices': GAME_OF_LIFE['indices'],
            'carrot': lambda x: x - 1
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)


    def test_rule_with_valid_ruleset_but_missing_indices(self):
        test_rule = {
            'banana': [(4, 2), (1, 2)],
            'ruleset': GAME_OF_LIFE['ruleset']
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)


    def test_rule_with_misshapen_indices_1(self):
        test_rule = {
            'indices': [
                (1, 2),
                [3, 4, 5],
                (6)
            ],
            'ruleset': GAME_OF_LIFE['ruleset']
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)


    def test_rule_with_misshapen_indices_2(self):
        test_rule = {
            'indices': [
                (1, 2, 3),
                (4, 5, 6),
                (7, 8, 9)
            ],
            'ruleset': GAME_OF_LIFE['ruleset']
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)


    def test_rule_with_misshapen_indices_3(self):
        test_rule = {
            'indices': [
                (
                    (1, -2),
                    (10, 20)
                ),
                (
                    (3, 4, 5),
                    (-30, 40)
                ),
                (
                    (6, -7, 8, 9),
                    (60, 70)
                )
            ],
            'ruleset': GAME_OF_LIFE['ruleset']
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)


    def test_rule_with_wrong_data_type_for_indices(self):
        test_rule = {
            'indices': [
                [1.2, 4.0],
                [-7.3, 9.1],
                [2.21, -3.42]
            ],
            'ruleset': GAME_OF_LIFE['ruleset']
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)


if __name__ == '__main__':
    unittest.main()
