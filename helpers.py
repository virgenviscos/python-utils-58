import functools
import logging
import random
import time
from typing import Any, Callable, Tuple, Type

logger = logging.getLogger("game_net")


class GameServerTimeout(Exception):
    """Raised when game telemetry or server sync fails."""
    pass


def respawn_retry(
    max_retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    retry_exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """Retries network requests using exponential backoff with ping-inspired jitter."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as exc:
                    attempts += 1
                    if attempts > max_retries:
                        logger.error(f"[NETWORK] Desync in {func.__name__}: Max retries ({max_retries}) reached.")
                        raise exc
                    
                    delay = min(max_delay, base_delay * (2 ** (attempts - 1)))
                    jitter = random.uniform(0.05, 0.25) * delay
                    total_sleep = delay + jitter
                    
                    logger.warning(
                        f"[NETWORK] Packet loss in '{func.__name__}'. "
                        f"Attempt {attempts}/{max_retries} failed ({exc}). Retrying in {total_sleep:.2f}s..."
                    )
                    time.sleep(total_sleep)
        return wrapper
    return decorator


@respawn_retry(max_retries=3, base_delay=0.1, retry_exceptions=(GameServerTimeout, ConnectionResetError))
def sync_player_state(player_id: str, state_data: dict) -> dict:
    """Syncs player inventory and state data with the server."""
    if random.choice([True, False]):
        raise GameServerTimeout(f"Handshake dropped for player {player_id}")
    return {"status": "synced", "player_id": player_id, "timestamp": time.time(), "payload": state_data}
