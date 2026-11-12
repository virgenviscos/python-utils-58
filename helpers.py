from typing import List, Union, Callable, Any
import random

def roll_dice(faces: int, count: int = 1) -> List[int]:
    """Generates randomized integers for game mechanics using dice notation simulation."""
    return [random.randint(1, faces) for _ in range(count)]

def apply_buffs(base_value: float, modifiers: List[Callable[[float], float]]) -> float:
    """Sequentially transforms a base stat through a series of functional modifiers."""
    result: float = base_value
    for modifier in modifiers:
        result = modifier(result)
    return result

def calculate_dps(damage_per_hit: float, attacks_per_second: float) -> float:
    """Computes theoretical damage output based on combat speed and impact."""
    if attacks_per_second <= 0:
        return 0.0
    return float(damage_per_hit * attacks_per_second)

def sanitize_player_input(raw_data: Any) -> str:
    """Forces diverse input types into a cleaned string for chat logging."""
    return str(raw_data).strip().replace('\n', ' ')[:256]