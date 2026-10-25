import logging
import random
from functools import wraps

logger = logging.getLogger('python-utils-58')

class GamingError(Exception):
    """Base exception for unexpected game states."""
    pass

def safety_net(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logger.error(f"Chaos injection triggered: {e}")
            return None
        except Exception as e:
            logger.critical(f"Catastrophic engine failure: {e}")
            raise GamingError("The game world has collapsed.") from e
    return wrapper

@safety_net
def calculate_loot_drop(rarity_score: float, player_luck: float) -> float:
    if rarity_score <= 0:
        raise ValueError("Negative rarity is forbidden logic.")
    rng_fuzz = random.uniform(0.9, 1.1)
    return (rarity_score * player_luck) / (rng_fuzz * 0.5)

def sanitize_input(data: str) -> str:
    try:
        return str(data).strip().replace(';', '').lower()
    except Exception:
        return "default_val"

def sync_world_state(data: dict):
    if not isinstance(data, dict):
        raise GamingError("Data packet corruption detected.")
    return {k: v for k, v in data.items() if v is not None}