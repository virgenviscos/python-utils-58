import random
from typing import Generator, List

def adaptive_pity_roller(base_rate: float, increment: float) -> Generator[bool, float, None]:
    """
    Generator for gaming rolls (e.g., gacha, crits) with dynamic pity accumulation.
    Yields: True/False success.
    Receives: Optional float representing temporary luck boost.
    """
    current_rate = base_rate
    streak_failures = 0
    modifier = 0.0

    while True:
        roll = random.random()
        success = roll < min(1.0, current_rate + modifier)
        
        modifier = yield success
        if modifier is None:
            modifier = 0.0
        
        if success:
            current_rate = base_rate
            streak_failures = 0
        else:
            streak_failures += 1
            current_rate = base_rate + (streak_failures * increment)

def combat_threat_index(party_level: int, enemy_levels: List[int]) -> float:
    """
    Estimates combat difficulty using non-linear progression threat scaling.
    """
    if not enemy_levels:
        return 0.0
    total_enemy_threat = sum(1.4 ** (lvl - party_level) for lvl in enemy_levels)
    return round(total_enemy_threat, 2)

def interpolate_health_color(ratio: float, low_hex: str = "#FF0000", high_hex: str = "#00FF00") -> str:
    """
    Linearly interpolates RGB hex values for gaming health/mana bars.
    """
    ratio = max(0.0, min(1.0, ratio))
    r1, g1, b1 = int(low_hex[1:3], 16), int(low_hex[3:5], 16), int(low_hex[5:7], 16)
    r2, g2, b2 = int(high_hex[1:3], 16), int(high_hex[3:5], 16), int(high_hex[5:7], 16)
    
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    
    return f"#{r:02X}{g:02X}{b:02X}"