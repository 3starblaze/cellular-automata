import pyglet
from pyglet.window import key
from pyglet.gl import GL_QUADS

from Controller import Controller


class Util:
    @staticmethod
    def corners_to_rect_coord(x1, y1, x2, y2):
        return [x1, y1, x1, y2, x2, y2, x2, y1]


class LocalController:
    def __init__(self, controller):
        if not issubclass(type(controller), Controller):
            raise ValueError("State is not an instance of StateMaintainer!")

        self.controller = controller
        self.window = pyglet.window.Window()

        @self.window.event
        def on_draw():
            self.window.clear()
            batch = pyglet.graphics.Batch()
            # drawing_objects = Drawer.draw(*self.window.get_size())
            w, h = self.window.get_size()
            self.controller.width = w
            self.controller.height = h
            drawing_objects = self.controller.drawing_data
            for line in drawing_objects["lines"]:
                batch.add(
                    4,
                    GL_QUADS,
                    None,
                    ("v2i", Util.corners_to_rect_coord(*line["coord"])),
                    ("c3B", self.controller.drawer.grid_line_color * 4),
                )
            for cell in drawing_objects["cells"]:
                if cell["state"]:
                    current_color = self.controller.drawer.grid_cell_color
                else:
                    current_color = self.controller.drawer.dead_cell_color

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
                self.controller.next_frame()

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            line_width = self.controller.drawer.line_width
            cell_size = self.controller.drawer.cell_size
            # Check if not line
            if (x % (line_width + cell_size)) == 0 or (
                y % (line_width + cell_size)
            ) == 0:
                return
            x_cell = x // (line_width + cell_size)
            y_cell = y // (line_width + cell_size)
            if (
                x_cell < self.controller.data.shape[1]
                and y_cell < self.controller.data.shape[0]
            ):
                self.controller.data[y_cell, x_cell] = not self.controller.data[
                    y_cell, x_cell
                ]

    def run(self):
        pyglet.app.run()
