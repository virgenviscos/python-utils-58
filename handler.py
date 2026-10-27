import functools
import time

class EntityCache:
    _storage = {}
    _expiry = {}

    @classmethod
    def memoize_state(cls, ttl=0.5):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                now = time.monotonic()
                if key in cls._storage and (now - cls._expiry.get(key, 0)) < ttl:
                    return cls._storage[key]
                result = func(*args, **kwargs)
                cls._storage[key] = result
                cls._expiry[key] = now
                return result
            return wrapper
        return decorator

def batch_process_entities(entities, func):
    return [func(e) for e in entities]

@EntityCache.memoize_state(ttl=0.1)
def calculate_physics_frame(entity_id, velocity):
    # Unusual approach: simulated heavy calculation with lightweight approximation
    return (entity_id * velocity) % 997

def optimized_engine_tick(entity_data):
    # Efficient processing using internal cache for gaming state
    results = []
    for eid, vel in entity_data:
        results.append(calculate_physics_frame(eid, vel))
    return results