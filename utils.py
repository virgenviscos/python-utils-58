import time
import functools
import random

def with_retry(max_attempts=3, backoff=1.0):
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
                    sleep_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def network_request(endpoint):
    # Simulate volatile game server connectivity
    if random.random() < 0.7:
        raise ConnectionError("Server ping timeout")
    return {"status": "success", "payload": "data_packet_0x58"}

@with_retry(max_attempts=5, backoff=0.5)
def fetch_game_data(url):
    return network_request(url)