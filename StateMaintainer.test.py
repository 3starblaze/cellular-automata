import unittest

from StateMaintainer import StateMaintainer

class TestStateMaintainer(unittest.TestCase):
    def test_incorrectly_shaped_1d_input(self):
        self.assertRaises(ValueError, StateMaintainer,
                          [False, False, True, False, True, True])


    def test_correctly_shaped_2d_input(self):
        try:
            StateMaintainer([[True, False, False],
                             [False, True, False],
                             [False, False, True]])
        except ValueError:
            self.fail("Correctly shapped array raises an exception!")


    def test_incorrectly_shaped_3d_input(self):
        self.assertRaises(ValueError, StateMaintainer,
                          [[[False, False]], [[True, False]], [[True, True]]])


if __name__ == '__main__':
    unittest.main()
