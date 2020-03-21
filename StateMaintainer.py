import numpy as np


class StateMaintainer:
    def __init__(self, data, rules):
        self.data = data
        self.rules = rules


    @property
    def data(self):
        return self.data


    @data.setter
    def data(self, value):
        temp_data = np.array(value)
        if temp_data.ndim != 2:
            raise ValueError("data expected in 2 dimensions; got {temp_data.ndim}")

        self._data = temp_data


    @property
    def rules(self):
        return self.rules

    @rules.setter
    def rules(self, value):
        if value == {}:
            raise ValueError("rules is empty!")
        self._rules = value
