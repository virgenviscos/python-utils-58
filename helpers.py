import time
import random
from typing import Any, Callable, Dict

def loot_generator(rarity_weights: Dict[str, float]) -> str:
    items = list(rarity_weights.keys())
    weights = list(rarity_weights.values())
    return random.choices(items, weights=weights, k=1)[0]

def throttle_events(interval: float = 0.5):
    def decorator(func: Callable):
        last_called = [0.0]
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed >= interval:
                last_called[0] = time.time()
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator

def normalize_coords(x: float, y: float, grid_size: int = 100) -> tuple:
    return (round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)

class StateContainer:
    def __init__(self):
        self._data = {}
    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)
    def __setitem__(self, key: str, value: Any):
        self._data[key] = value
    def purge(self) -> None:
        self._data.clear()