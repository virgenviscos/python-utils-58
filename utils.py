import time
import functools
import random
from typing import Callable, Any, Optional

def retry_network_op(max_attempts: int = 3, backoff_factor: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor * (2 ** attempt) + random.uniform(0, 0.1)
                        time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

def packet_resilience(max_retries: int = 5):
    def outer(func: Callable):
        @functools.wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if i == max_retries - 1:
                        raise
                    time.sleep(0.1 * (i + 1))
        return inner
    return outer