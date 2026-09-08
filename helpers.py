import random
import time
from functools import wraps

def jitter_delay(min_ms=50, max_ms=250):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(random.uniform(min_ms, max_ms) / 1000.0)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def loot_roll(chance):
    return random.random() < chance

def format_stats(data: dict, prefix: str = 'Gamer_'):
    return {f"{prefix}{k.upper()}": v for k, v in data.items()}

def throttle_events(interval):
    last_called = [0.0]
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed > interval:
                last_called[0] = time.time()
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator

class EntityPool:
    def __init__(self, size=10):
        self._pool = [None] * size
    def get_slot(self):
        idx = self._pool.index(None) if None in self._pool else -1
        return idx