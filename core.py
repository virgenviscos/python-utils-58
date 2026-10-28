import array
import math
from typing import Dict, Generator

class SpatialHashGrid:
    """Bitwise spatial hashing grid using typed arrays for fast game entity queries."""
    __slots__ = ('cell_size', 'shift', 'grid', 'mask')

    def __init__(self, cell_size: int = 64, grid_bits: int = 10) -> None:
        self.cell_size = cell_size
        self.shift = int(math.log2(cell_size)) if cell_size > 0 else 6
        self.mask = (1 << grid_bits) - 1
        self.grid: Dict[int, array.array] = {}

    def _hash(self, x: float, y: float) -> int:
        cx = int(x) >> self.shift
        cy = int(y) >> self.shift
        return ((cx & self.mask) << 10) | (cy & self.mask)

    def insert(self, entity_id: int, x: float, y: float) -> None:
        key = self._hash(x, y)
        bucket = self.grid.get(key)
        if bucket is None:
            bucket = array.array('I')
            self.grid[key] = bucket
        bucket.append(entity_id)

    def clear(self) -> None:
        self.grid.clear()

    def query_radius(self, x: float, y: float, radius: float) -> Generator[int, None, None]:
        min_cx = int(x - radius) >> self.shift
        max_cx = int(x + radius) >> self.shift
        min_cy = int(y - radius) >> self.shift
        max_cy = int(y + radius) >> self.shift

        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                key = ((cx & self.mask) << 10) | (cy & self.mask)
                bucket = self.grid.get(key)
                if bucket:
                    for eid in bucket:
                        yield eid

    def get_cell_stats(self) -> Dict[int, int]:
        return {key: len(buf) for key, buf in self.grid.items()}