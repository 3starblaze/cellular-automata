import numpy as np

from StateMaintainer import StateMaintainer
from GridDrawer import GridDrawer
from Rule import Rule


class Controller:
    """Provide a simple interface for cellular automata simulations."""

    def __init__(
        self, indices, ruleset, width=100, height=100, data=np.zeros((10, 10))
    ):
        """
        Parameters
        ----------
        indices : array_like
            List of relative indices that will be retrieved in rule applying process. Must be 2-D with shape of (_, 2).
        ruleset : function
            Parameters
            ----------
            cell : bool
                Value of the selected cell.
            retrieved_cells : array_like
                Array of bools, representing cell values retrieved using `indices` array. Same 1-D size as `indices`.

            Returns
            -------
            bool
                Final value of the cell after applying a rule.
        width, height : int, optional
            Drawing canvas size in pixels.
        data : array_like, optional
            Grid with cell values. Must be 2-D.
        """
        self.width = width
        self.height = height
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
        """Apply the rule and update data accordingly."""
        StateMaintainer.apply_rule()
        self._update_data(StateMaintainer.data)
