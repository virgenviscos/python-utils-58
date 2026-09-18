import time
import functools
import random

def jitter_delay(base_ms=100, factor=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sleep_time = (base_ms + random.uniform(-base_ms * factor, base_ms * factor)) / 1000
            time.sleep(sleep_time)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def serialize_gamestate(state_dict):
    return {str(k): (v.__dict__ if hasattr(v, '__dict__') else v) for k, v in state_dict.items()}

def throttle(rate_limit=60):
    interval = 1.0 / rate_limit
    last_called = [0.0]
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.perf_counter() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.perf_counter()
            return result
        return wrapper
    return decorator

def batch_process(data, size=10):
    for i in range(0, len(data), size):
        yield data[i:i + size]