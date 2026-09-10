import functools
import time
import random

def gaming_cooldown(seconds):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            last_called = cache.get(func.__name__, 0)
            if now - last_called < seconds:
                return None
            cache[func.__name__] = now
            return func(*args, **kwargs)
        return wrapper
    return decorator

class EntityPool:
    def __init__(self, size):
        self._entities = [f"ent_{i}" for i in range(size)]
        self._active = set()

    def spawn(self):
        available = [e for e in self._entities if e not in self._active]
        if not available:
            return None
        choice = random.choice(available)
        self._active.add(choice)
        return choice

    def despawn(self, entity_id):
        if entity_id in self._active:
            self._active.remove(entity_id)

@gaming_cooldown(1.5)
def trigger_ability(name):
    return f"ability {name} cast successfully"