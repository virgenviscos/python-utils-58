import functools
import time

class EntityCache:
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.data = {}
        self.order = []

    def get(self, key):
        if key in self.data:
            self.order.remove(key)
            self.order.append(key)
            return self.data[key]
        return None

    def set(self, key, value):
        if key in self.data:
            self.order.remove(key)
        elif len(self.data) >= self.capacity:
            oldest = self.order.pop(0)
            del self.data[oldest]
        self.data[key] = value
        self.order.append(key)

def fast_lookup(func):
    cache = EntityCache()
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        result = cache.get(key)
        if result is None:
            result = func(*args, **kwargs)
            cache.set(key, result)
        return result
    return wrapper

@fast_lookup
def compute_frame_logic(entity_id, delta):
    time.sleep(0.01)
    return f"processed_{entity_id}_{delta}"

class StateHandler:
    def update(self, entity_ids, delta):
        return [compute_frame_logic(eid, delta) for eid in entity_ids]