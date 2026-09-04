import math
import random
from typing import Any, Iterable, List

def lerp_range(start: float, end: float, steps: int) -> List[float]:
    return [start + (end - start) * (i / (steps - 1)) for i in range(steps)]

def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))

def shuffle_weighted(items: List[Any], weights: List[float]) -> List[Any]:
    indices = list(range(len(items)))
    shuffled = []
    while indices:
        choice = random.choices(indices, weights=[weights[i] for i in indices])[0]
        shuffled.append(items[choice])
        indices.remove(choice)
    return shuffled

def grid_snap(value: float, step: float) -> float:
    return round(value / step) * step

def polar_to_cartesian(radius: float, angle_rad: float):
    return radius * math.cos(angle_rad), radius * math.sin(angle_rad)

def hex_to_rgb(hex_code: str) -> tuple:
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def distance_sq(p1: tuple, p2: tuple) -> float:
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def chunk_list(data: Iterable, size: int) -> List[List[Any]]:
    it = iter(data)
    return [list(chunk) for chunk in iter(lambda: list(zip(*[it]*size)), [])]
