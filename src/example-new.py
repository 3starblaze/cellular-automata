from Controller import Controller
from LocalController import LocalController

import numpy as np
import random

my_list = np.array([random.choice([1, 0]) for i in range(20 ** 2)]).reshape(20, 20)


def GAME_OF_LIFE_RULESET(cell, values):
    if cell:
        return sum(values) >= 2 and sum(values) <= 3
    else:
        return sum(values) == 3

GAME_OF_LIFE_INDICES = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]

LocalController(Controller(GAME_OF_LIFE_INDICES, GAME_OF_LIFE_RULESET)).run()
