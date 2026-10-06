import functools
import time

class GameTickOptimizer:
    def __init__(self, cache_size=128):
        self.cache_size = cache_size
        self._memo = {}
        self._order = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self._memo:
                return self._memo[key]
            
            result = func(*args, **kwargs)
            
            if len(self._memo) >= self.cache_size:
                old_key = self._order.pop(0)
                del self._memo[old_key]
            
            self._memo[key] = result
            self._order.append(key)
            return result
        return wrapper

@GameTickOptimizer(cache_size=256)
def calculate_physics_vector(force, mass, delta_time):
    return (force / mass) * (delta_time ** 2) * 0.5

def process_game_loop(entities):
    start_time = time.perf_counter()
    results = [
        calculate_physics_vector(e.force, e.mass, 0.016)
        for e in entities
    ]
    execution_time = time.perf_counter() - start_time
    return results, execution_time