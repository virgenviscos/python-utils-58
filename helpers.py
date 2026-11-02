import functools
import time
import collections

CACHE_LIMIT = 128

class EntityCache:
    """High-performance entity state retrieval via LRU slotting."""
    def __init__(self, capacity=CACHE_LIMIT):
        self._storage = collections.OrderedDict()
        self.capacity = capacity

    def get_state(self, entity_id, fetch_func):
        if entity_id in self._storage:
            self._storage.move_to_end(entity_id)
            return self._storage[entity_id]
        
        state = fetch_func(entity_id)
        self._storage[entity_id] = state
        if len(self._storage) > self.capacity:
            self._storage.popitem(last=False)
        return state

def frame_throttle(delay_ms):
    """Execution frequency dampening for game loop events."""
    def decorator(func):
        last_called = 0
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            now = time.monotonic() * 1000
            if (now - last_called) >= delay_ms:
                last_called = now
                return func(*args, **kwargs)
        return wrapper
    return decorator

def fast_bitmask_check(mask, flag):
    """Bitwise validation for game state flags."""
    return (mask & flag) == flag

def batch_process_entities(entities, transform_func):
    """Generator-based memory-efficient entity transformation."""
    for entity in entities:
        yield transform_func(entity)