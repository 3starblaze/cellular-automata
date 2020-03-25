from GridDrawer import GridDrawer
from StateMaintainer import StateMaintainer

class Controller:
    def __init__(self, State, iterations):
        if not issubclass(type(State), StateMaintainer):
            raise ValueError("State is not an instance of StateMaintainer!")
        try:
            if iterations != int(iterations): raise ValueError()
        except ValueError:
            raise ValueError("iterations is not an integer")
        if iterations <= 0: raise ValueError("iterations is not positive!")

        self.State = State
        self.iterations = iterations

    def run(self):
        for i in range(self.iterations):
            GridDrawer(2, 30, self.State.data).start()
            self.State.apply_rules()
