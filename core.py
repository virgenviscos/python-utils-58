import math
from typing import Dict, List, Set, Tuple, Any

class SpatialHashGrid:
    """An optimized 2D spatial hash grid for ultra-fast proximity queries in 2D games."""
    __slots__ = ('cell_size', 'grid')

    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int], Set[Any]] = {}

    def _hash(self, x: float, y: float) -> Tuple[int, int]:
        # Fast bit-shifting approximation of division for power-of-two cell sizes
        size = self.cell_size
        if (size & (size - 1)) == 0:
            shift = size.bit_length() - 1
            return (int(x) >> shift, int(y) >> shift)
        return (int(x // size), int(y // size))

    def update(self, entity_id: Any, old_pos: Tuple[float, float], new_pos: Tuple[float, float]) -> None:
        """Updates an entity's position in the grid with minimal overhead."""
        old_key = self._hash(*old_pos)
        new_key = self._hash(*new_pos)
        
        if old_key != new_key:
            grid = self.grid
            if old_key in grid:
                grid[old_key].discard(entity_id)
                if not grid[old_key]:
                    del grid[old_key]
            
            if new_key not in grid:
                grid[new_key] = {entity_id}
            else:
                grid[new_key].add(entity_id)

    def insert(self, entity_id: Any, pos: Tuple[float, float]) -> None:
        key = self._hash(*pos)
        grid = self.grid
        if key not in grid:
            grid[key] = {entity_id}
        else:
            grid[key].add(entity_id)

    def remove(self, entity_id: Any, pos: Tuple[float, float]) -> None:
        key = self._hash(*pos)
        grid = self.grid
        if key in grid:
            grid[key].discard(entity_id)
            if not grid[key]:
                del grid[key]

    def get_nearby(self, pos: Tuple[float, float], radius: float) -> Set[Any]:
        """Returns all entity IDs within the cells intersecting the radius bounding box."""
        px, py = pos
        
        min_x, min_y = self._hash(px - radius, py - radius)
        max_x, max_y = self._hash(px + radius, py + radius)
        
        nearby: Set[Any] = set()
        grid = self.grid
        
        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                cell_key = (cx, cy)
                if cell_key in grid:
                    nearby.update(grid[cell_key])
        return nearby