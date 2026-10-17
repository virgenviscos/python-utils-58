import math
from typing import List, Dict, Set


class FastSpatialGrid:
    """High-performance spatial partitioning using bitwise coordinate packing."""

    __slots__ = ("cell_size", "shift", "grid")

    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self.shift = (cell_size & -cell_size).bit_length() - 1
        self.grid: Dict[int, Set[int]] = {}

    def _hash_coords(self, x: float, y: float) -> int:
        gx = int(x) >> self.shift
        gy = int(y) >> self.shift
        return (gx << 32) | (gy & 0xFFFFFFFF)

    def insert(self, entity_id: int, x: float, y: float) -> None:
        cell_key = self._hash_coords(x, y)
        if cell_key not in self.grid:
            self.grid[cell_key] = set()
        self.grid[cell_key].add(entity_id)

    def remove(self, entity_id: int, x: float, y: float) -> None:
        cell_key = self._hash_coords(x, y)
        if cell_key in self.grid:
            self.grid[cell_key].discard(entity_id)
            if not self.grid[cell_key]:
                del self.grid[cell_key]

    def query_radius(self, x: float, y: float, radius: float) -> List[int]:
        min_gx = int(x - radius) >> self.shift
        max_gx = int(x + radius) >> self.shift
        min_gy = int(y - radius) >> self.shift
        max_gy = int(y + radius) >> self.shift

        found: List[int] = []
        for gx in range(min_gx, max_gx + 1):
            for gy in range(min_gy, max_gy + 1):
                cell_key = (gx << 32) | (gy & 0xFFFFFFFF)
                if cell_key in self.grid:
                    found.extend(self.grid[cell_key])
        return found

    def clear(self) -> None:
        self.grid.clear()
