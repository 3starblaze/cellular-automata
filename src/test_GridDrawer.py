import random

import numpy as np
import pytest

from GridDrawer import GridDrawer

VALID_COLOR = (0, 100, 200)
VALID_DATA = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]


def test_negative_line_width():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(random.randint(-100, -1), 10, VALID_DATA)
    assert "line_width" in str(excinfo.value), "negative line_width is accepted"


def test_0_line_width():
    assert GridDrawer(0, 10, VALID_DATA), "line_width = 0 isn't accepted"


def test_negative_cell_size():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, random.randint(-100, -1), [])
    assert "cell_size" in str(excinfo.value), "negative cell_size is accepted"


def test_0_cell_size():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 0, [])
    assert "cell_size" in str(excinfo.value), "cell_size = 0 is accepted"


def test_data_getter():
    received_data = GridDrawer(2, 10, VALID_DATA).data
    np.testing.assert_equal(received_data, VALID_DATA)


def test_incorrectly_shaped_1d_input():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, [0, 0, 1, 0, 1, 1])
    assert "data" in str(excinfo.value), "1D data accepted"


def test_correctly_shaped_2d_input():
    GridDrawer(
        2, 10, [[True, False, False], [False, True, False], [False, False, True]],
    )
    assert True, "2D input not accepted"


def test_incorrectly_shaped_3d_input():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, [[[False, False]], [[True, False]], [[True, True]]])
    assert "data" in str(excinfo.value), "3D data accepted"


def test_incorect_color_format():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, VALID_DATA, "skrrr")
    assert "color format" in str(excinfo.value), "Wrong color format accepted"

    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, VALID_DATA, VALID_COLOR, 40)
    assert "color format" in str(excinfo.value), "Wrong color format accepted"


def test_incorrectly_shaped_color_tuples():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, VALID_DATA, (4, 2))
    assert "color format" in str(excinfo.value), "Wrongly shaped color format accepted"

    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, VALID_DATA, VALID_COLOR, (20, 40, 80, 20))
    assert "color format" in str(excinfo.value), "Wrongly shaped color format accepted"


def test_colors_with_invalid_numbers():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, VALID_DATA, (400, 20, 50))
    assert "color format" in str(
        excinfo.value
    ), "Color format with wrong integers accepted"

    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, VALID_DATA, VALID_COLOR, (-10, 80, 90))
    assert "color format" in str(
        excinfo.value
    ), "Color format with wrong integers accepted"


def test_colors_with_floats():
    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, VALID_DATA, (10.23, 20.21, 50))
    assert "color format" in str(excinfo.value), "Color format with floats accepted"

    with pytest.raises(ValueError) as excinfo:
        GridDrawer(2, 10, VALID_DATA, VALID_COLOR, (43.92, 123.45, 92.2))
    assert "color format" in str(excinfo.value), "Color format with floats accepted"


def test_drawer():
    data = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
    width, height = (10, 12)
    MyDrawer = GridDrawer(2, 4, data)
    returned_object = MyDrawer.draw(width, height)
    assert len(returned_object["lines"]) == 4, "Line count doesn't match"
    assert len(returned_object["cells"]) == 4, "Cell count doesn't match"
