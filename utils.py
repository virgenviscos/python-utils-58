import time
import functools
import random

def resilient_network_op(max_attempts=3, base_delay=1.0, backoff=2.0):
    """Decorator for network instability mitigation using exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = base_delay
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

def ping_game_server(url):
    """Simulated network call for gaming latency tests."""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Server node unreachable")
    return {"status": "ok", "latency": "24ms"}

@resilient_network_op(max_attempts=5)
def get_server_status(url):
    return ping_game_server(url)