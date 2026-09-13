import math
import random
from typing import Tuple, List

def pity_crit_roll(luck: float, misses: int, base_rate: float = 0.05) -> Tuple[bool, int]:
    """
    Calculates a critical hit outcome using an escalating pity-scaling factor.
    Returns a tuple of (is_critical, updated_miss_streak).
    """
    scaling = 1.0 + (luck / 100.0)
    escalation_rate = base_rate * math.pow(1.4, misses) * scaling
    
    if random.random() < min(escalation_rate, 1.0):
        return True, 0
    return False, misses + 1

def hex_neighbor_coords(q: int, r: int) -> List[Tuple[int, int]]:
    """
    Returns all neighboring coordinates on an axial hexagonal grid.
    """
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    return [(q + dq, r + dr) for dq, dr in directions]

def fibonacci_xp_threshold(level: int, base_xp: int = 100) -> int:
    """
    Generates gaming progression XP thresholds using an adjusted Binet's formula
    for golden-ratio scaling curves.
    """
    if level <= 0:
        return 0
    sqrt_five = 5 ** 0.5
    phi = (1 + sqrt_five) / 2
    psi = (1 - sqrt_five) / 2
    
    fib_value = (phi ** (level + 1) - psi ** (level + 1)) / sqrt_five
    return int(base_xp * round(fib_value))
