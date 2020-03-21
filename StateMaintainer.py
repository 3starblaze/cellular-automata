import numpy as np


class StateMaintainer:
    def __init__(self, data):
        self.data = data


    @property
    def data(self):
        return self.data


    @data.setter
    def data(self, value):
        temp_data = np.array(value)
        if temp_data.ndim != 2:
            raise ValueError("data expected in 2 dimensions; got {temp_data.ndim}")

        self._data = temp_data
