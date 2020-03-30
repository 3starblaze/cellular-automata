import unittest

from Controller import Controller
from StateMaintainer import StateMaintainer
from test_StateMaintainer import VALID_DATA, GAME_OF_LIFE

VALID_STATE_MAINTAINER = StateMaintainer(VALID_DATA, GAME_OF_LIFE)


class TestController(unittest.TestCase):
    def test_incorrect_data_type_for_State(self):
        self.assertRaisesRegex(ValueError, "State", Controller, "lasagna", 10)

    def test_incorrect_data_type_for_iterations(self):
        self.assertRaisesRegex(
            ValueError, "iterations", Controller, VALID_STATE_MAINTAINER, 4.72
        )

    def test_negative_iterations(self):
        self.assertRaisesRegex(
            ValueError, "iterations", Controller, VALID_STATE_MAINTAINER, -4
        )

    def test_0_iterations(self):
        self.assertRaisesRegex(
            ValueError, "iterations", Controller, VALID_STATE_MAINTAINER, 0
        )


if __name__ == "__main__":
    unittest.main()
