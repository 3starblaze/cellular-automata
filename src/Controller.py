import pyglet
from pyglet.gl import GL_QUADS

from GridDrawer import GridDrawer
from StateMaintainer import StateMaintainer


class Controller:
    def __init__(self, State, Drawer, iterations):
        if not issubclass(type(State), StateMaintainer):
            raise ValueError("State is not an instance of StateMaintainer!")

        try:
            if iterations != int(iterations):
                raise ValueError()
        except ValueError:
            raise ValueError("iterations is not an integer")
        if iterations <= 0:
            raise ValueError("iterations is not positive!")

        try:
            if not callable(Drawer.draw_grid) or not callable(Drawer.draw_cells):
                raise ValueError()
        except (ValueError, AttributeError) as e:
            raise ValueError(
                "`Drawer` doesn't have callable functions `draw_grid` and/or `draw_cells`"
            )

        self.State = State
        self.iterations = iterations

        # TODO Attach events that:
        # allow changing states while pushing keys

        self.window = pyglet.window.Window()

        @self.window.event
        def on_draw():
            self.window.clear()
            for line_tuple in Drawer.draw_grid(*self.window.get_size()):
                pyglet.graphics.draw(
                    4,
                    GL_QUADS,
                    ("v2i", line_tuple),
                    ("c3B", Drawer.grid_line_color * 4),
                )
            for cell_block in Drawer.draw_cells():
                pyglet.graphics.draw(
                    4,
                    GL_QUADS,
                    ("v2i", cell_block),
                    ("c3B", Drawer.grid_cell_color * 4),
                )

    def run(self):
        pyglet.app.run()
