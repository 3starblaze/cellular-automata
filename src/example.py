from StateMaintainer import StateMaintainer
from GridDrawer import GridDrawer
from Controller import Controller

my_list = np.array([random.choice([1, 0]) for i in range(20**2)]).reshape(20, 20)


def GAME_OF_LIFE_RULESET(cell, values):
    if cell:
        return sum(values) >= 2 and sum(values) <= 3
    else:
        return sum(values) == 3


GAME_OF_LIFE = {
    "indices": [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)],
    "ruleset": GAME_OF_LIFE_RULESET,
}


MyState = StateMaintainer(my_list, GAME_OF_LIFE)
MyDrawer = GridDrawer(1, 30, MyState.data)
MyController = Controller(MyState, MyDrawer)
MyController.run()
