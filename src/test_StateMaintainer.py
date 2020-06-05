import numpy as np
import pytest

from StateMaintainer import StateMaintainer
from Rule import Rule


def GAME_OF_LIFE_RULESET(cell, values):
    if cell:
        return sum(values) >= 2 and sum(values) <= 3
    else:
        return sum(values) == 3


# One of the valid rules
GAME_OF_LIFE = Rule(
    [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)],
    GAME_OF_LIFE_RULESET,
)

VALID_DATA = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]


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


# 'rule' argument tests
def test_rule_getter():
    received_rule = StateMaintainer(VALID_DATA, GAME_OF_LIFE).rule
    assert received_rule == GAME_OF_LIFE


def test_apply_rule():
    current_state = StateMaintainer(VALID_DATA, GAME_OF_LIFE)
    current_state.apply_rule()

    np.testing.assert_equal(
        current_state.data,
        [[False, False, False], [False, True, False], [False, False, False]],
    )


def test_apply_rule_2():
    current_state = StateMaintainer(
        [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 0]], GAME_OF_LIFE
    )
    current_state.apply_rule()

    np.testing.assert_equal(
        current_state.data, [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]]
    )
