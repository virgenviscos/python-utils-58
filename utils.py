import math
from typing import List, Tuple


class BitmaskSpatialGrid:
    """A lightweight 2D grid utilizing bitwise integer rows for spatial indexing."""

    def __init__(self, width: int, height: int, cell_size: float = 1.0):
        self.w = width
        self.h = height
        self.cell_size = cell_size
        self._bit_grid: List[int] = [0] * height

    def _coords_to_bit(self, x: float, y: float) -> Tuple[int, int]:
        col = int(math.floor(x / self.cell_size)) % self.w
        row = int(math.floor(y / self.cell_size)) % self.h
        return col, row

    def mark_entity(self, x: float, y: float) -> None:
        col, row = self._coords_to_bit(x, y)
        self._bit_grid[row] |= 1 << col

    def clear_entity(self, x: float, y: float) -> None:
        col, row = self._coords_to_bit(x, y)
        self._bit_grid[row] &= ~(1 << col)

    def is_occupied(self, x: float, y: float) -> bool:
        col, row = self._coords_to_bit(x, y)
        return bool(self._bit_grid[row] & (1 << col))

    def get_radius_occupancy(self, cx: float, cy: float, radius: float) -> List[Tuple[int, int]]:
        center_col, center_row = self._coords_to_bit(cx, cy)
        r_cells = int(math.ceil(radius / self.cell_size))
        occupied = []

        for r in range(max(0, center_row - r_cells), min(self.h, center_row + r_cells + 1)):
            row_bits = self._bit_grid[r]
            if not row_bits:
                continue
            for c in range(max(0, center_col - r_cells), min(self.w, center_col + r_cells + 1)):
                if (row_bits >> c) & 1:
                    dx = (c - center_col) * self.cell_size
                    dy = (r - center_row) * self.cell_size
                    if dx * dx + dy * dy <= radius * radius:
                        occupied.append((c, r))
        return occupied

    def render_ascii_map(self) -> str:
        return "\n".join(
            "".join("#" if (self._bit_grid[r] >> c) & 1 else "." for c in range(self.w))
            for r in range(self.h)
        )
