import functools
import time
import random

class GameResourceOrchestrator:
    def __init__(self, resource_pool=None):
        self._pool = resource_pool or set()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.purge_stale_entities()

    def purge_stale_entities(self):
        self._pool = {e for e in self._pool if hasattr(e, 'is_alive') and e.is_alive()}

    def execute_throttled(self, func, interval=0.05):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(interval * random.random())
            return func(*args, **kwargs)
        return wrapper

def validate_game_state(state_data):
    required = {'player_id', 'hp', 'coords'}
    return all(key in state_data for key in required)

def transform_coordinates(func):
    """Decorator for coordinate normalization in 2D space."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, tuple) and len(result) == 2:
            return (round(result[0], 2), round(result[1], 2))
        return result
    return wrapper

class EntityFactory:
    def create_unique_id(self):
        return f"ent_{int(time.time() * 1000)}_{random.randint(100, 999)}"