import pyglet

from GridDrawer import GridDrawer
from StateMaintainer import StateMaintainer


class Controller:
    def __init__(self, State, Drawer, iterations):
        if not issubclass(type(State), StateMaintainer):
            raise ValueError("State is not an instance of StateMaintainer!")

        try:
            if iterations != int(iterations):
                raise ValueError()
        except ValueError:
            raise ValueError("iterations is not an integer")
        if iterations <= 0:
            raise ValueError("iterations is not positive!")

        try:
            if callable(Drawer.draw_grid) and callable(Drawer.draw_cells):
                raise ValueError()
        except (ValueError, AttributeError) as e:
            raise ValueError(
                "`Drawer` doesn't have callable functions `draw_grid` and/or `draw_cells`"
            )

        self.State = State
        self.iterations = iterations

        # TODO Attach events that:
        # draw grid
        # allow changing states while pushing keys

    def run(self):
        pyglet.app.run()
