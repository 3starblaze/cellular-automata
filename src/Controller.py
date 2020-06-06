import pyglet
from pyglet.window import key
from pyglet.gl import GL_QUADS, GLubyte
import numpy as np

from GridDrawer import GridDrawer
from StateMaintainer import StateMaintainer


class Util:
    @staticmethod
    def corners_to_rect_coord(x1, y1, x2, y2):
        return [x1, y1, x1, y2, x2, y2, x2, y1]


class Controller:
    def __init__(self, State, Drawer):
        if not issubclass(type(State), StateMaintainer):
            raise ValueError("State is not an instance of StateMaintainer!")

        if not issubclass(type(Drawer), GridDrawer):
            raise ValueError("Drawer is not an instance of GridDrawer!")

        self.State = State

        self.window = pyglet.window.Window()

        @self.window.event
        def on_draw():
            self.window.clear()
            batch = pyglet.graphics.Batch()
            drawing_objects = Drawer.draw(*self.window.get_size())
            for line in drawing_objects["lines"]:
                batch.add(
                    4,
                    GL_QUADS,
                    None,
                    ("v2i", Util.corners_to_rect_coord(*line["coord"])),
                    ("c3B", Drawer.grid_line_color * 4),
                )
            for cell in drawing_objects["cells"]:
                if cell["state"]:
                    current_color = Drawer.grid_cell_color
                else:
                    current_color = Drawer.dead_cell_color

                batch.add(
                    4,
                    GL_QUADS,
                    None,
                    ("v2i", Util.corners_to_rect_coord(*cell["coord"])),
                    ("c3B", current_color * 4),
                )
            batch.draw()

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.RIGHT:
                State.apply_rule()
                Drawer.data = State.data

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            # Check if not line
            if (x / (Drawer.line_width + Drawer.cell_size)) % 1 == 0 or (
                y / (Drawer.line_width + Drawer.cell_size)
            ) % 1 == 0:
                return
            x_cell = x // (Drawer.line_width + Drawer.cell_size)
            y_cell = y // (Drawer.line_width + Drawer.cell_size)
            if x_cell < self.State.data.shape[1] and y_cell < self.State.data.shape[0]:
                self.State.data[y_cell, x_cell] = not self.State.data[y_cell, x_cell]
            Drawer.data = State.data

    def run(self):
        pyglet.app.run()
