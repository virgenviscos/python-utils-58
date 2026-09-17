import time
import random
from typing import Any, Callable

def loot_generator(pool: list, drop_rate: float = 0.05) -> Any:
    """Rolls the dice for epic loot simulation."""
    if random.random() < drop_rate:
        return random.choice(pool)
    return None

def frame_throttle(target_fps: int) -> Callable:
    """Decorator for restricting execution frequency per tick."""
    interval = 1.0 / target_fps
    def decorator(func: Callable) -> Callable:
        last_call = [0.0]
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed >= interval:
                last_call[0] = time.time()
                return func(*args, **kwargs)
        return wrapper
    return decorator

def sanitize_player_tag(name: str) -> str:
    """Removes toxic symbols and enforces standard casing."""
    return ''.join(c for c in name if c.isalnum() or c in '_-')[:16].capitalize()

def xp_calculator(base: int, level: int, modifier: float = 1.5) -> int:
    """Exponential growth logic for gaming progression."""
    return int(base * (level ** modifier))