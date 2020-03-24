import pyglet
from pyglet.gl import GL_LINES, GL_QUADS

class GridDrawer:
    def __init__(self, line_width, spacing, data,
                 grid_line_color=(0, 100, 100),
                 grid_cell_color=(114, 109, 168)):
        if line_width <= 0: raise ValueError(f"Invalid line_width: {line_width}")
        if spacing <= 0: raise ValueError(f"Invalid spacing: {spacing}")
        if (not isinstance(grid_line_color, tuple) or len(grid_line_color) != 3
            or min(grid_line_color) < 0 or max(grid_line_color) > 255
            or any(x % 1 != 0 for x in grid_line_color)):
            raise ValueError(f"Invalid grid_line_color format: {grid_line_color}")
        if (not isinstance(grid_cell_color, tuple) or len(grid_cell_color) != 3
            or min(grid_cell_color) < 0 or max(grid_cell_color) > 255
            or any(x % 1 != 0 for x in grid_cell_color)):
            raise ValueError(f"Invalid grid_cell_color format: {grid_cell_color}")


        self.window = pyglet.window.Window()
        self.width, self.height = self.window.get_size()

        self.line_width = line_width
        pyglet.gl.glLineWidth(self.line_width)
        self.spacing = spacing
        self.data = data

        self.grid_line_color = grid_line_color
        self.grid_cell_color = grid_cell_color


    def draw_grid(self):
        # Horizontal lines
        for i in range(0, self.height, self.spacing):
            pyglet.graphics.draw(4, GL_QUADS,
                                 ('v2i', (0, i,
                                          0, i + self.line_width,
                                          self.width, i + self.line_width,
                                          self.width, i)),
                                 ('c3B', self.grid_line_color * 4))
        # Vertical lines
        for i in range(0, self.width, self.spacing):
            pyglet.graphics.draw(4, GL_QUADS,
                                 ('v2i', (i, 0,
                                          i, self.height,
                                          i + self.line_width, self.height,
                                          i + self.line_width, 0)),
                                 ('c3B', self.grid_line_color * 4))


    def draw_cells(self):
        starting_points = []
        for i, row in enumerate(self.data):
            for j, elem in enumerate(row):
                if elem:
                    starting_points.append((j, i))

        for x, y in starting_points:
            cell_size = self.spacing - self.line_width
            point1 = (self.line_width * (x + 1) + cell_size * x,
                      self.line_width * (y + 1) + cell_size * y)
            point2 = (point1[0] + cell_size, point1[1])
            point3 = (point2[0], point2[1] + cell_size)
            point4 = (point3[0] - cell_size, point3[1])
            pyglet.graphics.draw(4, GL_QUADS,
                                 ('v2i', (*point1, *point2, *point3, *point4)),
                                 ('c3B', self.grid_cell_color * 4))


    def start(self):
        @self.window.event
        def on_draw():
            self.draw_grid()
            self.draw_cells()

        pyglet.app.run()
