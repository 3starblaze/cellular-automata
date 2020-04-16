import unittest
import random

import numpy as np

from GridDrawer import GridDrawer

VALID_COLOR = (0, 100, 200)
VALID_DATA = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]


class TestGridDrawer(unittest.TestCase):
    def test_negative_line_width(self):
        self.assertRaisesRegex(
            ValueError,
            "line_width",
            GridDrawer,
            random.randint(-100, -1),
            10,
            VALID_DATA,
        )

    def test_0_line_width(self):
        try:
            GridDrawer(0, 10, VALID_DATA)
        except ValueError:
            self.fail("0 line width raises an exception!")

    def test_negative_cell_size(self):
        self.assertRaisesRegex(
            ValueError, "cell_size", GridDrawer, 2, random.randint(-100, -1), []
        )

    def test_0_cell_size(self):
        self.assertRaisesRegex(ValueError, "cell_size", GridDrawer, 2, 0, [])

    def test_data_getter(self):
        received_data = GridDrawer(2, 10, VALID_DATA).data.tolist()
        self.assertEqual(received_data, VALID_DATA)

    def test_incorrectly_shaped_1d_input(self):
        self.assertRaisesRegex(
            ValueError,
            "data",
            GridDrawer,
            2,
            10,
            [False, False, True, False, True, True],
        )

    def test_correctly_shaped_2d_input(self):
        try:
            GridDrawer(
                2,
                10,
                [[True, False, False], [False, True, False], [False, False, True]],
            )
        except ValueError:
            self.fail("Correctly shapped array raises an exception!")

    def test_incorrectly_shaped_3d_input(self):
        self.assertRaisesRegex(
            ValueError,
            "data",
            GridDrawer,
            2,
            10,
            [[[False, False]], [[True, False]], [[True, True]]],
        )

    def test_incorect_color_format(self):
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, VALID_DATA, "skrrr"
        )
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, VALID_DATA, VALID_COLOR, 40
        )

    def test_incorrectly_shaped_color_tuples(self):
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, VALID_DATA, (4, 2)
        )
        self.assertRaisesRegex(
            ValueError,
            "color format",
            GridDrawer,
            2,
            10,
            VALID_DATA,
            VALID_COLOR,
            (20, 40, 80, 20),
        )

    def test_colors_with_invalid_numbers(self):
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, VALID_DATA, (400, 20, 50)
        )
        self.assertRaisesRegex(
            ValueError,
            "color format",
            GridDrawer,
            2,
            10,
            VALID_DATA,
            VALID_COLOR,
            (-10, 80, 90),
        )

    def test_colors_with_floats(self):
        self.assertRaisesRegex(
            ValueError,
            "color format",
            GridDrawer,
            2,
            10,
            VALID_DATA,
            (10.23, 20.21, 50),
        )
        self.assertRaisesRegex(
            ValueError,
            "color format",
            GridDrawer,
            2,
            10,
            VALID_DATA,
            VALID_COLOR,
            (43.92, 123.45, 92.2),
        )

    def test_random_line_count(self):
        cell_size = random.randint(1, 100)
        line_width = random.randint(1, 10)
        TestDrawer = GridDrawer(line_width, cell_size, VALID_DATA)

        grid_size = (random.randint(100, 1000), random.randint(100, 1000))
        self.assertEqual(
            len(TestDrawer.draw_grid(*grid_size)),
            (1 + (grid_size[0] - 1) // (line_width + cell_size))
            + (1 + (grid_size[1] - 1) // (line_width + cell_size)),
        )

    def test_random_cell_count(self):
        size = (random.randint(100, 1000), random.randint(100, 1000))
        data = [random.choice([1, 0]) for _ in range(size[0] * size[1])]
        data = np.array(data).reshape(*size)
        valid_cell_count = data.sum()

        cell_size = random.randint(1, 100)
        line_width = random.randint(1, 10)
        TestDrawer = GridDrawer(line_width, cell_size, data)
        self.assertEqual(len(TestDrawer.draw_cells()), valid_cell_count)


if __name__ == "__main__":
    unittest.main()
