import pyglet
from pyglet.window import key
from pyglet.gl import GL_QUADS, GLubyte
import numpy as np

from GridDrawer import GridDrawer
from StateMaintainer import StateMaintainer


class Controller:
    def __init__(self, State, Drawer):
        if not issubclass(type(State), StateMaintainer):
            raise ValueError("State is not an instance of StateMaintainer!")

        if not issubclass(type(Drawer), GridDrawer):
            raise ValueError("Drawer is not an instance of GridDrawer!")

        self.State = State

        self.window = pyglet.window.Window()
        self._drawn_image = pyglet.image.create(*self.window.get_size())
        self.drawn_data = Drawer.draw(*self.window.get_size())

        @self.window.event
        def on_draw():
            self.window.clear()
            self._drawn_image.blit(0, 0)

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.RIGHT:
                State.apply_rules()
                Drawer.data = State.data
                self.drawn_data = Drawer.draw(*self.window.get_size())

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            # Check if not line
            if np.array_equal(self.drawn_data[x, y], Drawer.grid_line_color):
                return
            x_cell = x // (Drawer.line_width + Drawer.cell_size)
            y_cell = y // (Drawer.line_width + Drawer.cell_size)
            self.State.data[y_cell, x_cell] = not self.State.data[y_cell, x_cell]
            Drawer.data = State.data
            self.drawn_data = Drawer.draw(*self.window.get_size())

    def _update_image(self):
        raw_data = (GLubyte * self._drawn_data.size)(
            *self._drawn_data.swapaxes(0, 1).flatten().astype("int")
        )
        self._drawn_image = pyglet.image.ImageData(
            *self._drawn_data.shape[:2], "RGB", raw_data
        )

    @property
    def drawn_data(self):
        return self._drawn_data

    @drawn_data.setter
    def drawn_data(self, value):
        self._drawn_data = value
        self._update_image()

    def run(self):
        pyglet.app.run()
