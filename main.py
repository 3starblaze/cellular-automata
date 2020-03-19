import pyglet
from pyglet.gl import GL_LINES


def draw_grid(spacing, width, height):
    # Horizontal lines
    for i in range(0, height, spacing):
        pyglet.graphics.draw(2, GL_LINES,
                              ('v2i', (0, i, width, i)))
    # Vertical lines
    for i in range(0, width, spacing):
        pyglet.graphics.draw(2, GL_LINES,
                              ('v2i', (i, 0, i, height)))


window = pyglet.window.Window()
w, h = window.get_size()

@window.event
def on_draw():
    draw_grid(10, w, h)

pyglet.app.run()
