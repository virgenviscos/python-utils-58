import time
import functools
import random

def exponential_backoff(retries=3, base_delay=1.0, max_delay=10.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= retries:
                        raise e
                    sleep_time = min(max_delay, base_delay * (2 ** (attempts - 1))) + random.uniform(0, 0.5)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkThrottler:
    def __init__(self, limit=5):
        self.limit = limit
        self.calls = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            self.calls = [t for t in self.calls if now - t < 1]
            if len(self.calls) >= self.limit:
                time.sleep(0.1)
            self.calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper