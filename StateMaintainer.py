import numpy as np


class StateMaintainer:
    def __init__(self, data):
        data = np.array(data)
        if data.ndim != 2:
            raise ValueError("data expected in 2 dimensions; got {data.ndim}")

        self.data = np.array(data)
