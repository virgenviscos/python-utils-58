import functools
import collections

class EntityCache:
    """High-speed entity lookup using double-decker LRU architecture."""
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.hot_cache = {}
        self.cold_cache = collections.OrderedDict()

    def get_entity(self, entity_id, fetch_func):
        if entity_id in self.hot_cache:
            return self.hot_cache[entity_id]
        
        if entity_id in self.cold_cache:
            val = self.cold_cache.pop(entity_id)
            self._promote(entity_id, val)
            return val

        val = fetch_func(entity_id)
        self._promote(entity_id, val)
        return val

    def _promote(self, key, value):
        self.hot_cache[key] = value
        if len(self.hot_cache) > self.capacity:
            k, v = self.hot_cache.popitem()
            self.cold_cache[k] = v

@functools.lru_cache(maxsize=128)
def calculate_collision_vector(pos_a, pos_b):
    """Vectorized-style spatial calculation optimization."""
    dx, dy = pos_a[0] - pos_b[0], pos_a[1] - pos_b[1]
    return (dx**2 + dy**2)**0.5

def batch_process_entities(entities, transform_func):
    """Generator-based pipeline for memory efficiency."""
    for entity in entities:
        yield transform_func(entity)

class StateProcessor:
    def __init__(self):
        self.registry = EntityCache()
    
    def update(self, entity_id, data):
        return self.registry.get_entity(entity_id, lambda x: data)