import pyglet
from pyglet.window import key
from pyglet.gl import GL_QUADS, GLubyte

from GridDrawer import GridDrawer
from StateMaintainer import StateMaintainer


class Controller:
    def __init__(self, State, Drawer):
        if not issubclass(type(State), StateMaintainer):
            raise ValueError("State is not an instance of StateMaintainer!")

        try:
            if not callable(Drawer.draw_grid) or not callable(Drawer.draw_cells):
                raise ValueError()
        except (ValueError, AttributeError) as e:
            raise ValueError(
                "`Drawer` doesn't have callable functions `draw_grid` and/or `draw_cells`"
            )

        self.State = State

        self.window = pyglet.window.Window()
        self._drawn_data = Drawer.draw(*self.window.get_size())

        @self.window.event
        def on_draw():
            self.window.clear()
            # data needs to be in ctype, otherwise can't be blitted
            raw_data = (GLubyte * self._drawn_data.size)(
                *self._drawn_data.flatten().astype("int")
            )
            y, x = self._drawn_data.shape[:2]
            img = pyglet.image.ImageData(x, y, "RGB", raw_data)
            img.blit(0, 0)

        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.RIGHT:
                State.apply_rules()
                Drawer.data = State.data
                self._drawn_data = Drawer.draw(*self.window.get_size())

    def run(self):
        pyglet.app.run()
