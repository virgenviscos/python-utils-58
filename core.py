import time
import random
from typing import Callable, Any

def frame_rate_throttle(target_fps: float) -> Callable:
    interval = 1.0 / target_fps
    def decorator(func: Callable) -> Callable:
        last_call = [0.0]
        def wrapper(*args, **kwargs):
            now = time.perf_counter()
            elapsed = now - last_call[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            last_call[0] = time.perf_counter()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def loot_generator(pool: dict[str, float]) -> str:
    items = list(pool.keys())
    weights = list(pool.values())
    return random.choices(items, weights=weights, k=1)[0]

def coordinate_mapper(x: int, y: int, grid_size: int = 1024) -> int:
    return (x << 16) | (y & 0xFFFF)

def sanitize_player_input(text: str) -> str:
    return ''.join(c for c in text if c.isalnum() or c in ' _-').strip()[:32]

class EntityRegistry:
    def __init__(self):
        self._storage = {}

    def __setitem__(self, key: int, value: Any):
        self._storage[key] = value

    def __getitem__(self, key: int) -> Any:
        return self._storage.get(key)