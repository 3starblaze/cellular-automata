import unittest
import random

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
        self.assertRaisesRegex(ValueError, "line_width", GridDrawer, 0, 10, VALID_DATA)

    def test_negative_spacing(self):
        self.assertRaisesRegex(
            ValueError, "spacing", GridDrawer, 2, random.randint(-100, -1), VALID_DATA
        )

    def test_0_spacing(self):
        self.assertRaisesRegex(ValueError, "spacing", GridDrawer, 2, 0, VALID_DATA)

    def test_incorrect_data_type(self):
        self.assertRaisesRegex(ValueError, "data", GridDrawer, 2, 10, "meow")

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


if __name__ == "__main__":
    unittest.main()
