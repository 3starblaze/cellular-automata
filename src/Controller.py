import numpy as np

from StateMaintainer import StateMaintainer
from GridDrawer import GridDrawer
from Rule import Rule


class Controller:
    """Provide a simple interface for cellular automata simulations."""

    def __init__(self, indices, ruleset, width=100, height=100, data=None):
        self.width = width
        self.height = height
        if not data:
            self.data = np.zeros((10, 10))
        else:
            self.data = data
        self.state = StateMaintainer(self.data, Rule(indices, ruleset))
        self.drawer = GridDrawer(2, 30, self.data)
        self.drawing_data = {}

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("`width` is not positive!")
        elif value % 1 != 0:
            raise ValueError("`width` is not an integer")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("`height` is not positive!")
        elif value % 1 != 0:
            raise ValueError("`height` is not an integer")
        self._height = value

    def _update_data(self, data):
        self.state.data = data
        self.drawer.data = data
        self.drawing_data = self.drawer.draw(self.width, self.height)

    def next_frame(self):
        StateMaintainer.apply_rule()
        self._update_data(StateMaintainer.data)
