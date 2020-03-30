import unittest
import copy

import numpy as np

from StateMaintainer import StateMaintainer


def GAME_OF_LIFE_RULESET(cell, values):
    if cell:
        return sum(values) >= 2 and sum(values) <= 3
    else:
        return sum(values) == 3


# One of the valid rules
GAME_OF_LIFE = {
    "indices": [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)],
    "ruleset": GAME_OF_LIFE_RULESET,
}

VALID_DATA = [[False, False, True], [False, True, False], [True, False, False]]


class TestStateMaintainer(unittest.TestCase):
    # 'data' argument tests
    def test_data_getter(self):
        received_data = StateMaintainer(VALID_DATA, GAME_OF_LIFE).data.tolist()
        self.assertEqual(received_data, VALID_DATA)

    def test_incorrectly_shaped_1d_input(self):
        self.assertRaises(
            ValueError,
            StateMaintainer,
            [False, False, True, False, True, True],
            GAME_OF_LIFE,
        )

    def test_correctly_shaped_2d_input(self):
        try:
            StateMaintainer(
                [[True, False, False], [False, True, False], [False, False, True]],
                GAME_OF_LIFE,
            )
        except ValueError:
            self.fail("Correctly shapped array raises an exception!")

    def test_incorrectly_shaped_3d_input(self):
        self.assertRaises(
            ValueError,
            StateMaintainer,
            [[[False, False]], [[True, False]], [[True, True]]],
            GAME_OF_LIFE,
        )

    # 'rules' argument tests
    def test_rules_getter(self):
        received_rules = StateMaintainer(VALID_DATA, GAME_OF_LIFE).rules
        received_rules["indices"] = received_rules["indices"].tolist()
        expected_rules = copy.deepcopy(GAME_OF_LIFE)
        expected_rules["indices"] = np.array(expected_rules["indices"]).tolist()
        self.assertEqual(received_rules, expected_rules)

    def test_correct_rule(self):
        try:
            StateMaintainer(VALID_DATA, GAME_OF_LIFE)
        except ValueError:
            self.fail("Correct rule raises an exception!")

    def test_empty_rule(self):
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, {})

    def test_rule_with_invalid_keys(self):
        test_rule = {"banana": [(4, 2), (1, 2)], "carrot": lambda x: x - 1}
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_valid_indices_but_missing_ruleset(self):
        test_rule = {"indices": GAME_OF_LIFE["indices"], "carrot": lambda x: x - 1}
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_valid_ruleset_but_missing_indices(self):
        test_rule = {"banana": [(4, 2), (1, 2)], "ruleset": GAME_OF_LIFE["ruleset"]}
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_misshapen_indices_1(self):
        test_rule = {
            "indices": [(1, 2), [3, 4, 5], (6)],
            "ruleset": GAME_OF_LIFE["ruleset"],
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_misshapen_indices_2(self):
        test_rule = {
            "indices": [(1, 2, 3), (4, 5, 6), (7, 8, 9)],
            "ruleset": GAME_OF_LIFE["ruleset"],
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_misshapen_indices_3(self):
        test_rule = {
            "indices": [
                ((1, -2), (10, 20)),
                ((3, 4, 5), (-30, 40)),
                ((6, -7, 8, 9), (60, 70)),
            ],
            "ruleset": GAME_OF_LIFE["ruleset"],
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_wrong_data_type_for_indices(self):
        test_rule = {
            "indices": [[1.2, 4.0], [-7.3, 9.1], [2.21, -3.42]],
            "ruleset": GAME_OF_LIFE["ruleset"],
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_wrong_data_type_for_rulesest(self):
        test_rule = {"indices": GAME_OF_LIFE["indices"], "ruleset": "fun"}
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_wrong_ruleset_with_1_parameter(self):
        test_rule = {"indices": GAME_OF_LIFE["indices"], "ruleset": lambda x: x}
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_correct_ruleset_with_3_parameters(self):
        test_rule = {
            "indices": GAME_OF_LIFE["indices"],
            "ruleset": lambda x, y, z: x + y + z,
        }
        self.assertRaises(ValueError, StateMaintainer, VALID_DATA, test_rule)

    def test_rule_with_extra_data(self):
        test_rule = copy.deepcopy(GAME_OF_LIFE)
        test_rule["extra1"] = "junk"
        test_rule["extra2"] = [0, 0, 7]

        # Converting 'indices' to normal lists because of numpy's '=='
        received_rule = StateMaintainer(VALID_DATA, test_rule).rules
        received_rule["indices"] = received_rule["indices"].tolist()
        expected_rule = StateMaintainer(VALID_DATA, GAME_OF_LIFE).rules
        expected_rule["indices"] = expected_rule["indices"].tolist()

        self.assertEqual(received_rule, expected_rule)

    def test_apply_rules(self):
        current_state = StateMaintainer(VALID_DATA, GAME_OF_LIFE)
        current_state.apply_rules()

        self.assertTrue(
            np.array_equal(
                current_state.data,
                [[False, False, False], [False, True, False], [False, False, False]],
            )
        )

    def test_apply_rules_2(self):
        current_state = StateMaintainer(
            [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]], GAME_OF_LIFE
        )
        current_state.apply_rules()

        self.assertTrue(
            np.array_equal(
                current_state.data,
                [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]],
            )
        )


if __name__ == "__main__":
    unittest.main()
