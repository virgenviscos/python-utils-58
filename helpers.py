import random
import time
from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class NetworkGlitched(Exception):
    """Raised when game server connection fails continuously."""

    pass


class ExtraLivesRetry:
    """Retry policy modeled as player extra lives with cooldown respawn buffers."""

    def __init__(
        self,
        lives: int = 3,
        cooldown_base: float = 0.5,
        jitter_range: tuple = (0.1, 0.4),
        catch_exceptions: tuple = (Exception,),
    ):
        self.lives = lives
        self.cooldown_base = cooldown_base
        self.jitter_range = jitter_range
        self.catch_exceptions = catch_exceptions

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def respawn_wrapper(*args: Any, **kwargs: Any) -> T:
            lives_left = self.lives
            attempt = 0
            while lives_left > 0:
                try:
                    return func(*args, **kwargs)
                except self.catch_exceptions as err:
                    lives_left -= 1
                    attempt += 1
                    if lives_left <= 0:
                        raise NetworkGlitched(
                            f"Operation '{func.__name__}' game over after {self.lives} retries: {err}"
                        ) from err

                    cooldown = (self.cooldown_base * (2 ** (attempt - 1))) + random.uniform(
                        *self.jitter_range
                    )
                    time.sleep(cooldown)
            raise NetworkGlitched("Unexpected failure in respawn loop")

        return respawn_wrapper


def net_retry(lives: int = 3, base_delay: float = 0.5):
    """Convenience decorator for network state synchronization retries."""
    return ExtraLivesRetry(lives=lives, cooldown_base=base_delay)
