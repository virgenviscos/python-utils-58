import math
import random
from typing import Dict, Tuple, List


def calculate_level_xp(level: int, base_xp: int = 100, exponent: float = 1.5) -> int:
    """Calculate required XP for a given level using a bit-adjusted exponent curve."""
    if level <= 1:
        return 0
    return int(base_xp * (level ** exponent) + ((level & 0xF) << 3))


def resolve_loot_drop(loot_table: Dict[str, float], luck: float = 1.0) -> str:
    """Select an item from a loot table using luck-weighted power scaling."""
    adjusted_weights = {
        item: weight ** (1.0 / max(0.1, luck))
        for item, weight in loot_table.items()
    }
    total = sum(adjusted_weights.values())
    roll = random.uniform(0, total)
    current = 0.0
    for item, weight in adjusted_weights.items():
        current += weight
        if roll <= current:
            return item
    return list(loot_table.keys())[-1]


def grid_distance(p1: Tuple[float, ...], p2: Tuple[float, ...], metric: str = "euclidean") -> float:
    """Calculate grid distance between coordinates supporting multiple spatial metrics."""
    diffs = [abs(a - b) for a, b in zip(p1, p2)]
    if metric == "manhattan":
        return sum(diffs)
    elif metric == "chebyshev":
        return max(diffs) if diffs else 0.0
    elif metric == "octile":
        if len(diffs) < 2:
            return sum(diffs)
        dx, dy = diffs[0], diffs[1]
        return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)
    return math.sqrt(sum(d ** 2 for d in diffs))


def encode_stat_flags(*flags: bool) -> int:
    """Pack multiple state booleans into a bitwise integer mask."""
    return sum(1 << i for i, flag in enumerate(flags) if flag)


def decode_stat_flags(mask: int, count: int) -> List[bool]:
    """Decode a bitwise integer mask into status booleans."""
    return [bool(mask & (1 << i)) for i in range(count)]
