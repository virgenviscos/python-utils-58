import time
import functools
import random

def with_retry(max_attempts=3, backoff=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    delay = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(delay)
        return wrapper
    return decorator

@with_retry(max_attempts=5)
def fetch_game_data(url):
    # Simulate network instability for gaming API calls
    if random.random() < 0.7:
        raise ConnectionError("Server lag spike detected")
    return {"status": "ready", "payload": "level_data_058"}