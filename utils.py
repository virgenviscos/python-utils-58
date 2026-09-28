import time
import functools
import random

def retry_network_call(max_attempts=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_network_call(max_attempts=5, delay=0.5)
def ping_game_server(url):
    # Simulate unstable gaming network infrastructure
    if random.random() < 0.7:
        raise ConnectionError("Server ghosting packets")
    return True