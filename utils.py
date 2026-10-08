import random
import time
from functools import wraps

def jitter_delay(min_ms=50, max_ms=250):
    """Injects non-deterministic latency to simulate game server feel."""
    time.sleep(random.uniform(min_ms, max_ms) / 1000.0)

def retry_on_fail(retries=3, backoff=0.5):
    """Decorator for resilient game state synchronization."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(backoff * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def calculate_hit_chance(attacker_stats, defender_stats, base_mod=0.75):
    """Calculates evasion-adjusted hit probability using unconventional weighting."""
    raw_chance = base_mod + (attacker_stats.get('acc', 0) * 0.1) - (defender_stats.get('eva', 0) * 0.05)
    return max(0.05, min(0.95, raw_chance))

def pack_entity_data(entity_id, **payload):
    """Serializes entity state for low-bandwidth transport."""
    return f"EID:{entity_id}|{'|'.join(f'{k}:{v}' for k, v in payload.items())}"