import pytest
import numpy as np

from Rule import Rule


def GAME_OF_LIFE_RULESET(cell, values):
    if cell:
        return sum(values) >= 2 and sum(values) <= 3
    else:
        return sum(values) == 3


GAME_OF_LIFE_INDICES = [
    (-1, 1),
    (0, 1),
    (1, 1),
    (-1, 0),
    (1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
]


def test_indices_getter():
    rule = Rule(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET)
    assert np.array_equal(rule.indices, GAME_OF_LIFE_INDICES)


def test_misshapen_indices_1():
    indices = [(1, 2), [3, 4, 5], (6)]
    with pytest.raises(ValueError):
        Rule(indices, GAME_OF_LIFE_RULESET)


def test_misshapen_indices_2():
    indices = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    with pytest.raises(ValueError):
        Rule(indices, GAME_OF_LIFE_RULESET)


def test_misshapen_indices_3():
    indices = [
        ((1, -2), (10, 20)),
        ((3, 4, 5), (-30, 40)),
        ((6, -7, 8, 9), (60, 70)),
    ]
    with pytest.raises(ValueError):
        Rule(indices, GAME_OF_LIFE_RULESET)


def test_wrong_data_type_for_indices():
    indices = [[1.2, 4.0], [-7.3, 9.1], [2.21, -3.42]]

    with pytest.raises(ValueError):
        Rule(indices, GAME_OF_LIFE_RULESET)


def test_ruleset_getter():
    rule = Rule(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET)
    assert rule.ruleset == GAME_OF_LIFE_RULESET


def test_wrong_data_type_for_ruleset():
    with pytest.raises(ValueError):
        Rule(GAME_OF_LIFE_INDICES, "fun")


def test_ruleset_with_2_parameters():
    Rule(GAME_OF_LIFE_INDICES, lambda cell, values: cell and values)
    assert True


def test_rule_with_ruleset_that_operates_on_explicit_indices():
    Rule(GAME_OF_LIFE_INDICES, lambda cell, values: values[6])
    assert True
