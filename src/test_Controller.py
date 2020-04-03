import unittest

from Controller import Controller
from GridDrawer import GridDrawer
from StateMaintainer import StateMaintainer
from test_StateMaintainer import VALID_DATA, GAME_OF_LIFE

VALID_STATE_MAINTAINER = StateMaintainer(VALID_DATA, GAME_OF_LIFE)
VALID_GRID_DRAWER = GridDrawer(2, 10, [])


class TestController(unittest.TestCase):
    def test_correct_arguments(self):
        try:
            Controller(
                VALID_STATE_MAINTAINER, VALID_GRID_DRAWER,
            )
        except ValueError:
            self.fail("Correct arguments raise an exception!")

    def test_incorrect_data_type_for_State(self):
        self.assertRaisesRegex(
            ValueError, "State", Controller, "lasagna", VALID_GRID_DRAWER,
        )

    def test_incorrect_drawer(self):
        self.assertRaisesRegex(
            ValueError, "Drawer", Controller, VALID_STATE_MAINTAINER, "burger",
        )

    def test_object_with_variables_that_should_be_functions(self):
        self.assertRaisesRegex(
            ValueError,
            "Drawer",
            Controller,
            VALID_STATE_MAINTAINER,
            {"draw_grid": False, "draw_cells": [2, 40, 41],},
        )

    def test_object_with_variables_that_should_be_functions(self):
        class Object(object):
            pass

        test_obj = Object()
        test_obj.draw_grid = lambda x: "hey"
        test_obj.draw_cells = lambda: "oh"

        try:
            Controller(
                VALID_STATE_MAINTAINER, test_obj,
            )
        except ValueError:
            self.fail("Correct object raises an exception!")


if __name__ == "__main__":
    unittest.main()
