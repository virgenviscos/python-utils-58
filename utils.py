import time
import random
import functools
from typing import Callable, Any

def backoff_retry(max_retries: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    # jittered exponential backoff for game network resilience
                    sleep_time = (base_delay * (2 ** (retries - 1))) + (random.random() * 0.1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@backoff_retry(max_retries=5)
def fetch_game_state(endpoint: str):
    # simulates network jitter in gaming scenarios
    if random.random() < 0.7:
        raise ConnectionError("packet loss detected")
    return {"status": "ready", "tick": 128}