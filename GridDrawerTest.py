import unittest
import random

from GridDrawer import GridDrawer

VALID_COLOR = (0, 100, 200)


class TestGridDrawer(unittest.TestCase):
    def test_negative_line_width(self):
        self.assertRaisesRegex(
            ValueError, "line_width", GridDrawer, random.randint(-100, -1), 10, []
        )

    def test_0_line_width(self):
        self.assertRaisesRegex(ValueError, "line_width", GridDrawer, 0, 10, [])

    def test_negative_spacing(self):
        self.assertRaisesRegex(
            ValueError, "spacing", GridDrawer, 2, random.randint(-100, -1), []
        )

    def test_0_spacing(self):
        self.assertRaisesRegex(ValueError, "spacing", GridDrawer, 2, 0, [])

    def test_incorect_color_format(self):
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, [], "skrrr"
        )
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, [], VALID_COLOR, 40
        )

    def test_incorrectly_shaped_color_tuples(self):
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, [], (4, 2)
        )
        self.assertRaisesRegex(
            ValueError,
            "color format",
            GridDrawer,
            2,
            10,
            [],
            VALID_COLOR,
            (20, 40, 80, 20),
        )

    def test_colors_with_invalid_numbers(self):
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, [], (400, 20, 50)
        )
        self.assertRaisesRegex(
            ValueError,
            "color format",
            GridDrawer,
            2,
            10,
            [],
            VALID_COLOR,
            (-10, 80, 90),
        )

    def test_colors_with_floats(self):
        self.assertRaisesRegex(
            ValueError, "color format", GridDrawer, 2, 10, [], (10.23, 20.21, 50)
        )
        self.assertRaisesRegex(
            ValueError,
            "color format",
            GridDrawer,
            2,
            10,
            [],
            VALID_COLOR,
            (43.92, 123.45, 92.2),
        )


if __name__ == "__main__":
    unittest.main()
