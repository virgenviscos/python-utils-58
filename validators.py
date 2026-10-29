"""Validation pipelines for gaming mechanics and entity attributes."""

from typing import Any, Callable, List, Tuple, Union

Number = Union[int, float]
Coord = Tuple[Number, Number, Number]


class ValidatorPipeline:
    """Composable validator stream for game entity state verification."""

    def __init__(self, target_name: str):
        self.target_name = target_name
        self.rules: List[Callable[[Any], bool]] = []

    def clamp_range(self, min_val: Number, max_val: Number) -> "ValidatorPipeline":
        self.rules.append(
            lambda v: isinstance(v, (int, float)) and min_val <= v <= max_val
        )
        return self

    def spatial_bounds(self, box_min: Coord, box_max: Coord) -> "ValidatorPipeline":
        def _check(pos: Any) -> bool:
            if not isinstance(pos, (tuple, list)) or len(pos) != 3:
                return False
            return all(box_min[i] <= pos[i] <= box_max[i] for i in range(3))

        self.rules.append(_check)
        return self

    def bitmask_flags(self, required_flags: int) -> "ValidatorPipeline":
        self.rules.append(
            lambda mask: isinstance(mask, int) and (mask & required_flags) == required_flags
        )
        return self

    def validate(self, value: Any) -> bool:
        for rule in self.rules:
            if not rule(value):
                raise ValueError(
                    f"Validation failed for attribute '{self.target_name}' with value: {value}"
                )
        return True


def sanitize_character_name(name: str, max_len: int = 16) -> str:
    """Strips non-alphanumeric gaming handles and enforces length limits."""
    cleaned = "".join(c for c in name if c.isalnum() or c in "_-")
    if not cleaned or len(cleaned) > max_len:
        raise ValueError(f"Invalid character name: '{name}'")
    return cleaned
