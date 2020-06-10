import numpy as np

from Rule import Rule


class StateMaintainer:
    """Store 2d cell data and apply rule functions to data."""

    def __init__(self, data, rule):
        """
        Parameters
        ----------
        data : array_like
            Grid with cell values. Must be 2-D.
        rule : Rule
            Rules that are going to be applied to data.
        """
        self.data = data
        self.rule = rule

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        temp_data = np.array(value)
        if temp_data.ndim != 2:
            raise ValueError(f"data expected in 2 dimensions; got {temp_data.ndim}")

        self._data = temp_data

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, value):
        if not issubclass(type(value), Rule):
            raise ValueError("`rule` is not an instance of `Rule`")
        self._rule = value

    def apply_rule(self):
        """Use ruleset function on data and update data."""

        def relative_to_absolute_coord(cur_x, cur_y):
            return [(cur_x + xi, cur_y + yi) for xi, yi in self.rule.indices]

        def coordinates_in_bounds(x, y):
            if min(x, y) < 0:
                return False
            if x >= self.data.shape[0]:
                return False
            if y >= self.data.shape[1]:
                return False
            return True

        new_data = np.zeros(self.data.shape)
        it = np.nditer(self.data, flags=["multi_index"])
        while not it.finished:
            values_from_coords = []
            for xi, yi in relative_to_absolute_coord(*it.multi_index):
                if not coordinates_in_bounds(xi, yi):
                    values_from_coords.append(False)
                else:
                    values_from_coords.append(self.data[xi, yi])

            new_data[it.multi_index] = self.rule.ruleset(it[0], values_from_coords)
            it.iternext()

        self.data = new_data
