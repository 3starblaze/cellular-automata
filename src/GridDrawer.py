import math
import numpy as np
from PIL import Image, ImageDraw


class Util:
    @staticmethod
    def validate_color(color):
        return (
            isinstance(color, tuple)
            and len(color) == 3
            and min(color) >= 0
            and max(color) <= 255
            and all(x % 1 == 0 for x in color)
        )


class GridDrawer:
    """Draw 2-D data in a grid."""

    def __init__(
        self,
        line_width,
        cell_size,
        data,
        grid_line_color=(0, 100, 100),
        grid_cell_color=(114, 109, 168),
        dead_cell_color=(0, 0, 0),
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
        dead_cell_color: tuple of ints, optional
            Color of cells that are not alive.
        """
        self.line_width = line_width
        self.cell_size = cell_size
        self.data = data
        self.grid_line_color = grid_line_color
        self.grid_cell_color = grid_cell_color
        self.dead_cell_color = dead_cell_color
        self._drawing_payload = {}

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        if value < 0:
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
        if not Util.validate_color(value):
            raise ValueError(f"Invalid grid_line_color format: {value}")
        else:
            self._grid_line_color = value

    @property
    def grid_cell_color(self):
        return self._grid_cell_color

    @grid_cell_color.setter
    def grid_cell_color(self, value):
        if not Util.validate_color(value):
            raise ValueError(f"Invalid grid_cell_color format: {value}")
        else:
            self._grid_cell_color = value

    @property
    def dead_cell_color(self):
        return self._dead_cell_color

    @dead_cell_color.setter
    def dead_cell_color(self, value):
        if not Util.validate_color(value):
            raise ValueError(f"Invalid dead_cell_color format: {value}")
        else:
            self._dead_cell_color = value

    def draw_grid(self, width, height):
        if self.line_width == 0:
            return

        lines = []
        # Horizontal lines
        for i in range(0, height, self.cell_size + self.line_width):
            lines.append({"coord": [0, i, width, i + self.line_width]})

        # Vertical lines
        for i in range(0, width, self.cell_size + self.line_width):
            lines.append({"coord": [i, 0, i + self.line_width, height]})

        self._drawing_payload["lines"] = lines

    def draw_cells(self, width, height):
        cells = []
        # Calculate max values (same formula as in loop below)
        x_max = min(
            self.data.shape[0],
            math.ceil((width - self.line_width) / (self.line_width + self.cell_size)),
        )
        y_max = min(
            self.data.shape[1],
            math.ceil((height - self.line_width) / (self.line_width + self.cell_size)),
        )
        for x in range(x_max):
            for y in range(y_max):
                x1 = self.line_width * (x + 1) + self.cell_size * x
                y1 = self.line_width * (y + 1) + self.cell_size * y
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cells.append(
                    {"coord": [x1, y1, x2, y2], "state": self.data[x, y],}
                )

        self._drawing_payload["cells"] = cells

    def draw(self, width, height):
        self.draw_grid(width, height)
        self.draw_cells(width, height)

        return self._drawing_payload
