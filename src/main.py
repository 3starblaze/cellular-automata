from StateMaintainer import StateMaintainer
from Controller import Controller

my_list = [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0]]


def GAME_OF_LIFE_RULESET(cell, values):
    if not cell:
        return sum(values) >= 2 and sum(values) <= 3
    else:
        return sum(values) == 3


GAME_OF_LIFE = {
    "indices": [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)],
    "ruleset": GAME_OF_LIFE_RULESET,
}


MyState = StateMaintainer(my_list, GAME_OF_LIFE)
Controller(MyState, 10).run()
