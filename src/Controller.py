from StateMaintainer import StateMaintainer
from GridDrawer import GridDrawer
from Rule import Rule


class Controller:
    """Provide a simple interface for cellular automata simulations."""

    def __init__(self, indices, ruleset, data=None):
        self.data = data
        self.state = StateMaintainer(data, Rule(indices, ruleset))
        self.drawer = GridDrawer(2, 30, data)
        self.drawing_data = {}

    def _update_data(self, data, width, height):
        self.state.data = data
        self.drawer.data = data
        self.drawing_data = self.drawer.draw(width, height)

    def next_frame(self, width, height):
        StateMaintainer.apply_rule()
        self._update_data(StateMaintainer.data, width, height)
