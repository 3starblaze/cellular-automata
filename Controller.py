from GridDrawer import GridDrawer

class Controller:
    def __init__(self, State, iterations):
        self.State = State
        self.iterations = iterations

    def run(self):
        for i in range(self.iterations):
            GridDrawer(2, 30, self.State.data).start()
            self.State.apply_rules()
