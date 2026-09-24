import random
import time

def roll_dice(sides: int = 6) -> int:
    return random.randint(1, sides)

def throttle_calls(interval: float):
    def decorator(func):
        last_called = [0.0]
        def wrapper(*args, **kwargs):
            elapsed = time.perf_counter() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.perf_counter()
            return result
        return wrapper
    return decorator

def memoize_game_state(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize_game_state
def calculate_damage(base: int, multiplier: float) -> int:
    return int(base * multiplier)

@throttle_calls(0.1)
def sync_server_packet(payload: dict):
    print(f"dispatching packet: {payload}")
    return True

def sanitize_player_input(text: str) -> str:
    return ''.join(c for c in text if c.isalnum() or c in ' !?').strip()