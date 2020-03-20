import unittest
import random

from GridDrawer import GridDrawer

class TestGridDrawer(unittest.TestCase):
    def test_negative_line_width(self):
        self.assertRaisesRegex(ValueError, "line_width", GridDrawer,
                               random.randint(-100, -1), 10, [])

    def test_0_line_width(self):
        self.assertRaisesRegex(ValueError, "line_width", GridDrawer,
                               0, 10, [])

    def test_negative_spacing(self):
        self.assertRaisesRegex(ValueError, "spacing", GridDrawer,
                               2, random.randint(-100, -1), [])

    def test_negative_spacing(self):
        self.assertRaisesRegex(ValueError, "spacing", GridDrawer,
                               2, 0, [])


if __name__ == '__main__':
    unittest.main()
