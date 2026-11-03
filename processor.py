from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass(frozen=True)
class ItemTile:
    name: str
    shape: Tuple[complex, ...]  # Offsets using complex numbers (1j = Y-axis, 1 = X-axis)

class InventoryGrid:
    """Spatial inventory grid processor using complex number arithmetic for rotations."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.occupied: Dict[complex, str] = {}

    @staticmethod
    def rotate_shape(shape: Tuple[complex, ...], degrees: int) -> Tuple[complex, ...]:
        """Rotates shape offsets via complex multiplication by powers of 1j."""
        rotations = (degrees % 360) // 90
        factor = (1j) ** rotations
        return tuple(complex(round((pt * factor).real), round((pt * factor).imag)) for pt in shape)

    def can_place(self, item: ItemTile, origin: complex, degrees: int = 0) -> bool:
        rotated_shape = self.rotate_shape(item.shape, degrees)
        for offset in rotated_shape:
            target = origin + offset
            x, y = int(target.real), int(target.imag)
            if not (0 <= x < self.width and 0 <= y < self.height):
                return False
            if target in self.occupied:
                return False
        return True

    def place_item(self, item: ItemTile, x: int, y: int, degrees: int = 0) -> bool:
        origin = complex(x, y)
        if not self.can_place(item, origin, degrees):
            return False
        
        for offset in self.rotate_shape(item.shape, degrees):
            self.occupied[origin + offset] = item.name
        return True

    def export_layout(self) -> List[Dict[str, float]]:
        """Serializes layout state into normalized vector telemetry data."""
        return [
            {
                "item": name,
                "norm_x": round(pos.real / self.width, 4),
                "norm_y": round(pos.imag / self.height, 4)
            }
            for pos, name in self.occupied.items()
        ]
