import numpy as np


class StateMaintainer:
    """Store 2d cell data and apply rule functions to data."""

    def __init__(self, data, rules):
        """
        :param data: 2d data, that can be converted to 2d np.array
        :param rules: object with keys "indices" and "rules"
            :param indices: n by 2 integer 2d array where each each element
                represents index, relative to origin cell
            :param ruleset: function (or callable) that takes 2 arguments:
                original cell value and cell value list (with same length as
                'indices') and which returns a new cell value.
        """
        self.data = data
        self.rules = rules

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        temp_data = np.array(value)
        if temp_data.ndim != 2:
            raise ValueError("data expected in 2 dimensions; got {temp_data.ndim}")

        self._data = temp_data

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        # indices
        if not "indices" in value:
            raise ValueError("'rules' is missing 'indices'!")
        value["indices"] = np.array(value["indices"])

        if value["indices"].ndim != 2 or value["indices"].shape[1] != 2:
            raise ValueError("Misshapen 'indices'!")
        if value["indices"].dtype != "int64":
            raise ValueError("Invalid data type for 'indices'")

        # ruleset
        if not "ruleset" in value:
            raise ValueError("'rules' is missing 'ruleset'!")
        if not callable(value["ruleset"]):
            raise ValueError("Ruleset is not callable!")
        try:
            value["ruleset"](True, [False, True, True])
        except TypeError:
            raise ValueError("Ruleset doesn't accept 2 arguments!")

        self._rules = {"indices": value["indices"], "ruleset": value["ruleset"]}

    def apply_rules(self):
        def relative_to_absolute_coord(cur_x, cur_y):
            return [(cur_x + xi, cur_y + yi) for xi, yi in self.rules["indices"]]

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

            new_data[it.multi_index] = self.rules["ruleset"](it[0], values_from_coords)
            it.iternext()

        self.data = new_data
