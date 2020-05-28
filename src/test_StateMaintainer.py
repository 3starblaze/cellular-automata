import copy

import numpy as np
import pytest

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


# 'data' argument tests
def test_data_getter():
    received_data = StateMaintainer(VALID_DATA, GAME_OF_LIFE).data
    np.testing.assert_equal(received_data, VALID_DATA)


def test_incorrectly_shaped_1d_input():
    with pytest.raises(ValueError):
        StateMaintainer([False, False, True, False, True, True], GAME_OF_LIFE)


def test_correctly_shaped_2d_input():
    StateMaintainer(
        [[True, False, False], [False, True, False], [False, False, True]],
        GAME_OF_LIFE,
    )
    assert True


def test_incorrectly_shaped_3d_input():
    with pytest.raises(ValueError):
        StateMaintainer(
            [[[False, False]], [[True, False]], [[True, True]]], GAME_OF_LIFE
        )


# 'rules' argument tests
def test_rules_getter():
    received_rules = StateMaintainer(VALID_DATA, GAME_OF_LIFE).rules
    expected_rules = copy.deepcopy(GAME_OF_LIFE)
    np.testing.assert_equal(received_rules, expected_rules)


def test_correct_rule():
    StateMaintainer(VALID_DATA, GAME_OF_LIFE)
    assert True


def test_empty_rule():
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, {})


def test_rule_with_invalid_keys():
    test_rule = {"banana": [(4, 2), (1, 2)], "carrot": lambda x: x - 1}
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_valid_indices_but_missing_ruleset():
    test_rule = {"indices": GAME_OF_LIFE["indices"], "carrot": lambda x: x - 1}
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_valid_ruleset_but_missing_indices():
    test_rule = {"banana": [(4, 2), (1, 2)], "ruleset": GAME_OF_LIFE["ruleset"]}
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_misshapen_indices_1():
    test_rule = {
        "indices": [(1, 2), [3, 4, 5], (6)],
        "ruleset": GAME_OF_LIFE["ruleset"],
    }
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_misshapen_indices_2():
    test_rule = {
        "indices": [(1, 2, 3), (4, 5, 6), (7, 8, 9)],
        "ruleset": GAME_OF_LIFE["ruleset"],
    }
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_misshapen_indices_3():
    test_rule = {
        "indices": [
            ((1, -2), (10, 20)),
            ((3, 4, 5), (-30, 40)),
            ((6, -7, 8, 9), (60, 70)),
        ],
        "ruleset": GAME_OF_LIFE["ruleset"],
    }
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_wrong_data_type_for_indices():
    test_rule = {
        "indices": [[1.2, 4.0], [-7.3, 9.1], [2.21, -3.42]],
        "ruleset": GAME_OF_LIFE["ruleset"],
    }
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_wrong_data_type_for_rulesest():
    test_rule = {"indices": GAME_OF_LIFE["indices"], "ruleset": "fun"}
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_wrong_ruleset_with_1_parameter():
    test_rule = {"indices": GAME_OF_LIFE["indices"], "ruleset": lambda x: x}
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_correct_ruleset_with_3_parameters():
    test_rule = {
        "indices": GAME_OF_LIFE["indices"],
        "ruleset": lambda x, y, z: x + y + z,
    }
    with pytest.raises(ValueError):
        StateMaintainer(VALID_DATA, test_rule)


def test_rule_with_ruleset_that_operates_on_explicit_indices():
    test_rule = {
        "indices": GAME_OF_LIFE["indices"],
        "ruleset": lambda cell, values: values[6],
    }
    StateMaintainer(VALID_DATA, test_rule)
    assert True


def test_rule_with_extra_data():
    test_rule = copy.deepcopy(GAME_OF_LIFE)
    test_rule["extra1"] = "junk"
    test_rule["extra2"] = [0, 0, 7]

    received_rule = StateMaintainer(VALID_DATA, test_rule).rules
    expected_rule = StateMaintainer(VALID_DATA, GAME_OF_LIFE).rules

    np.testing.assert_equal(received_rule, expected_rule)


def test_apply_rules():
    current_state = StateMaintainer(VALID_DATA, GAME_OF_LIFE)
    current_state.apply_rules()

    np.testing.assert_equal(
        current_state.data,
        [[False, False, False], [False, True, False], [False, False, False]],
    )


def test_apply_rules_2():
    current_state = StateMaintainer(
        [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]], GAME_OF_LIFE
    )
    current_state.apply_rules()

    np.testing.assert_equal(
        current_state.data, [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]]
    )
