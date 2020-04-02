import unittest

from Controller import Controller
from GridDrawer import GridDrawer
from StateMaintainer import StateMaintainer
from test_StateMaintainer import VALID_DATA, GAME_OF_LIFE

VALID_STATE_MAINTAINER = StateMaintainer(VALID_DATA, GAME_OF_LIFE)
VALID_GRID_DRAWER = GridDrawer(2, 10, [])
VALID_ITERATIONS = 10


class TestController(unittest.TestCase):
    def test_correct_arguments(self):
        try:
            Controller(
                VALID_STATE_MAINTAINER, VALID_GRID_DRAWER, VALID_ITERATIONS,
            )
        except ValueError:
            self.fail("Correct arguments raise an exception!")

    def test_incorrect_data_type_for_State(self):
        self.assertRaisesRegex(
            ValueError,
            "State",
            Controller,
            "lasagna",
            VALID_GRID_DRAWER,
            VALID_ITERATIONS,
        )

    def test_incorrect_drawer(self):
        self.assertRaisesRegex(
            ValueError,
            "Drawer",
            Controller,
            VALID_STATE_MAINTAINER,
            "burger",
            VALID_ITERATIONS,
        )

    def test_object_with_variables_that_should_be_functions(self):
        self.assertRaisesRegex(
            ValueError,
            "Drawer",
            Controller,
            VALID_STATE_MAINTAINER,
            {"draw_grid": False, "draw_cells": [2, 40, 41],},
            VALID_ITERATIONS,
        )

    def test_object_with_variables_that_should_be_functions(self):
        class Object(object):
            pass

        test_obj = Object()
        test_obj.draw_grid = lambda x: "hey"
        test_obj.draw_cells = lambda: "oh"

        try:
            Controller(
                VALID_STATE_MAINTAINER, test_obj, VALID_ITERATIONS,
            )
        except ValueError:
            self.fail("Correct object raises an exception!")

    def test_incorrect_data_type_for_iterations(self):
        self.assertRaisesRegex(
            ValueError,
            "iterations",
            Controller,
            VALID_STATE_MAINTAINER,
            VALID_GRID_DRAWER,
            4.72,
        )

    def test_negative_iterations(self):
        self.assertRaisesRegex(
            ValueError,
            "iterations",
            Controller,
            VALID_STATE_MAINTAINER,
            VALID_GRID_DRAWER,
            -4,
        )

    def test_0_iterations(self):
        self.assertRaisesRegex(
            ValueError,
            "iterations",
            Controller,
            VALID_STATE_MAINTAINER,
            VALID_GRID_DRAWER,
            0,
        )


if __name__ == "__main__":
    unittest.main()
