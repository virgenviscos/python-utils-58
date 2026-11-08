import math
import random
from enum import IntFlag
from typing import Dict, Tuple, List, Optional


class StatusFlags(IntFlag):
    NONE = 0
    POISONED = 1 << 0
    STUNNED = 1 << 1
    FROZEN = 1 << 2
    BURNING = 1 << 3
    BLEEDING = 1 << 4
    INVULNERABLE = 1 << 5


def calculate_level_progression(xp: int, base: float = 100.0, growth: float = 1.25) -> Tuple[int, int]:
    """Calculates current level and remaining experience points required for the next level."""
    if xp <= 0:
        return 1, int(base)
    level = int(math.floor(math.log((xp / base) * (growth - 1) + 1, growth))) + 1
    xp_next_level = int(base * (math.pow(growth, level) - 1) / (growth - 1))
    return level, max(0, xp_next_level - xp)


def calculate_hex_distance(start: Tuple[int, int, int], end: Tuple[int, int, int]) -> int:
    """Calculates Manhattan distance between two tiles using 3D cube coordinates (x, y, z)."""
    return max(abs(start[0] - end[0]), abs(start[1] - end[1]), abs(start[2] - end[2]))


class PityLootTable:
    """Loot rolling utility with cumulative pity probability scaling for rare items."""

    def __init__(self, items: Dict[str, float], rare_keys: Optional[List[str]] = None):
        self.items = items
        self.rare_keys = set(rare_keys or [k for k in items if "epic" in k.lower() or "rare" in k.lower()])
        self.miss_counter = 0

    def roll(self, pity_step: float = 0.02) -> str:
        bonus = self.miss_counter * pity_step
        weights = []
        keys = list(self.items.keys())
        for key in keys:
            weight = self.items[key]
            if key in self.rare_keys:
                weight += bonus
            weights.append(max(0.0, weight))

        chosen = random.choices(keys, weights=weights, k=1)[0]
        if chosen in self.rare_keys:
            self.miss_counter = 0
        else:
            self.miss_counter += 1
        return chosen


def apply_status_modifier(current: StatusFlags, add: StatusFlags = StatusFlags.NONE, remove: StatusFlags = StatusFlags.NONE) -> StatusFlags:
    """Applies status flags while filtering invulnerability rules."""
    updated = (current | add) & ~remove
    if updated & StatusFlags.INVULNERABLE:
        updated &= ~(StatusFlags.POISONED | StatusFlags.BLEEDING | StatusFlags.BURNING)
    return updated
