import pytest

from Controller import Controller


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


def test_Controller_with_just_rules():
    Controller(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET)
    assert True


def test_negative_width():
    with pytest.raises(ValueError) as excinfo:
        Controller(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET, width=-20)
    assert "width" in str(excinfo.value)


def test_0_width():
    with pytest.raises(ValueError) as excinfo:
        Controller(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET, width=0)
    assert "width" in str(excinfo.value)


def test_float_width():
    with pytest.raises(ValueError) as excinfo:
        Controller(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET, width=72.8)
    assert "width" in str(excinfo.value)


def test_negative_height():
    with pytest.raises(ValueError) as excinfo:
        Controller(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET, height=-42)
    assert "height" in str(excinfo.value)


def test_0_height():
    with pytest.raises(ValueError) as excinfo:
        Controller(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET, height=0)
    assert "height" in str(excinfo.value)


def test_float_height():
    with pytest.raises(ValueError) as excinfo:
        Controller(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET, height=92.3)
    assert "height" in str(excinfo.value)
