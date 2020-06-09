from StateMaintainer import StateMaintainer
from GridDrawer import GridDrawer
from Rule import Rule


class Controller:
    """Provide a simple interface for cellular automata simulations."""

    def __init__(self, indices, ruleset, width=100, height=100, data=None):
        self.width = width
        self.height = height
        self.data = data
        self.state = StateMaintainer(data, Rule(indices, ruleset))
        self.drawer = GridDrawer(2, 30, data)
        self.drawing_data = {}

    def _update_data(self, data):
        self.state.data = data
        self.drawer.data = data
        self.drawing_data = self.drawer.draw(self.width, self.height)

    def next_frame(self):
        StateMaintainer.apply_rule()
        self._update_data(StateMaintainer.data)
