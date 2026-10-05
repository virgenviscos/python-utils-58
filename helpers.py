import time
import functools
from typing import Callable, Any

def gaming_cooldown(seconds: float):
    def decorator(func: Callable):
        last_called = 0
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            elapsed = time.time() - last_called
            if elapsed < seconds:
                return None
            last_called = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def loot_generator(items: list[str], weights: list[int]) -> str:
    import random
    return random.choices(items, weights=weights, k=1)[0]

class StateContainer:
    def __init__(self):
        self._data = {}
    
    def __setitem__(self, key, value):
        self._data[key] = value
        
    def __getitem__(self, key):
        return self._data.get(key, 0)
    
    def flush(self):
        self._data.clear()

def format_stats(xp: int, gold: int) -> str:
    return f"| LVL: {xp // 1000} | GP: {gold} |"