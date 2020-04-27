import numpy as np
from PIL import Image, ImageDraw


class GridDrawer:
    """Draw 2-D data in a grid."""

    def __init__(
        self,
        line_width,
        cell_size,
        data,
        grid_line_color=(0, 100, 100),
        grid_cell_color=(114, 109, 168),
    ):
        """
        Parameters
        ----------
        line_width : int
            Grid line width in px.
        cell_size : int
            Cell size in px.
        data : array_like
            2-D array of values that will be drawn by GridDrawer.
        grid_line_color: tuple of ints, optional
             Grid line color in 3 element RGB tuple.
        grid_cell_color: tuple of ints, optional
             Color of cells in 3 element RGB tuple that are represented by
             `true` in data.
        """
        self.line_width = line_width
        self.cell_size = cell_size
        self.data = data
        self.grid_line_color = grid_line_color
        self.grid_cell_color = grid_cell_color
        self._drawn_data = np.array([])

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        if value <= 0:
            raise ValueError(f"Invalid line_width: {value}")
        else:
            self._line_width = value

    @property
    def cell_size(self):
        return self._cell_size

    @cell_size.setter
    def cell_size(self, value):
        if value <= 0:
            raise ValueError(f"Invalid cell_size: {value}")
        else:
            self._cell_size = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        temp_data = np.array(value)
        if temp_data.ndim != 2:
            raise ValueError("data expected in 2 dimensions; got {temp_data.ndim}")

        self._data = temp_data.T

    @property
    def grid_line_color(self):
        return self._grid_line_color

    @grid_line_color.setter
    def grid_line_color(self, value):
        if (
            not isinstance(value, tuple)
            or len(value) != 3
            or min(value) < 0
            or max(value) > 255
            or any(x % 1 != 0 for x in value)
        ):
            raise ValueError(f"Invalid grid_line_color format: {value}")
        else:
            self._grid_line_color = value

    @property
    def grid_cell_color(self):
        return self._grid_cell_color

    @grid_cell_color.setter
    def grid_cell_color(self, value):
        if (
            not isinstance(value, tuple)
            or len(value) != 3
            or min(value) < 0
            or max(value) > 255
            or any(x % 1 != 0 for x in value)
        ):
            raise ValueError(f"Invalid grid_cell_color format: {value}")
        else:
            self._grid_cell_color = value

    def draw_grid(self, width, height):
        grid_lines = []
        # Horizontal lines
        for i in range(0, height, self.cell_size + self.line_width):
            self._drawn_data[0:width, i : i + self.line_width] = self.grid_line_color

        # Vertical lines
        for i in range(0, width, self.cell_size + self.line_width):
            self._drawn_data[i : i + self.line_width, 0:height] = self.grid_line_color

        return grid_lines

    def draw_cells(self):
        x, y = np.nonzero(self.data)
        for i in range(len(x)):
            x1 = self.line_width * (x[i] + 1) + self.cell_size * x[i]
            y1 = self.line_width * (y[i] + 1) + self.cell_size * y[i]
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            self._drawn_data[x1:x2, y1:y2] = self.grid_cell_color

    def draw(self, width, height):
        self._drawn_data = np.zeros((width, height, 3))
        self.draw_grid(width, height)
        self.draw_cells()

        return self._drawn_data
