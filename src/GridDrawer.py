import numpy as np


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
        """
        self.line_width = line_width
        self.cell_size = cell_size
        self.data = data
        self.grid_line_color = grid_line_color
        self.grid_cell_color = grid_cell_color
        self.dead_cell_color = dead_cell_color

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
            self._grid_cell_color = value

    def draw_grid(self, width, height):
        if self.line_width == 0:
            return []
        grid_lines = []
        # Horizontal lines
        for i in range(0, height, self.cell_size + self.line_width):
            grid_lines.append(
                (0, i, 0, i + self.line_width, width, i + self.line_width, width, i)
            )

        # Vertical lines
        for i in range(0, width, self.cell_size + self.line_width):
            grid_lines.append(
                (i, 0, i, height, i + self.line_width, height, i + self.line_width, 0)
            )

        return grid_lines

    def draw_cells(self):
        starting_points = []
        for i, row in enumerate(self.data):
            for j, elem in enumerate(row):
                if elem:
                    starting_points.append((j, i))

        cell_blocks = []
        for x, y in starting_points:
            point1 = (
                self.line_width * (x + 1) + self.cell_size * x,
                self.line_width * (y + 1) + self.cell_size * y,
            )
            point2 = (point1[0] + self.cell_size, point1[1])
            point3 = (point2[0], point2[1] + self.cell_size)
            point4 = (point3[0] - self.cell_size, point3[1])

            cell_blocks.append((*point1, *point2, *point3, *point4))

        return cell_blocks
