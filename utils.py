import time
import functools
import random

def retry_network_call(max_retries=3, base_delay=1.0, jitter=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == max_retries:
                        raise e
                    
                    sleep_time = base_delay * (2 ** (attempt - 1))
                    if jitter:
                        sleep_time *= (0.5 + random.random())
                    
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class NetworkHandler:
    @staticmethod
    @retry_network_call(max_retries=5)
    def sync_game_state(payload):
        print(f"Syncing: {payload}")
        # Simulation of unstable network
        if random.random() < 0.7:
            raise ConnectionError("Server lag detected")
        return True