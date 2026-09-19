import time
import functools
import random

def retry_gaming_network(max_attempts=3, backoff=0.5):
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
                    jitter = random.uniform(0, 0.1)
                    wait_time = (backoff * (2 ** (attempts - 1))) + jitter
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator

class LatencyValidator:
    @staticmethod
    @retry_gaming_network(max_attempts=3)
    def check_ping(target_ip):
        # Simulate a network socket ping in a gaming context
        if random.random() < 0.7:
            raise ConnectionError(f"server {target_ip} timed out")
        return True