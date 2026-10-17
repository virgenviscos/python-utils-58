import random
import time
from typing import Callable, Any, Type, Tuple


class ServerLagException(Exception):
    """Raised when a game server sync packet fails to transmit."""
    pass


class NetworkRetryHandler:
    """Network request handler using game-inspired exponential backoff with ping jitter."""

    def __init__(
        self,
        max_respawn_attempts: int = 5,
        base_cooldown: float = 0.2,
        multiplier: float = 1.8,
        jitter_bounds: Tuple[float, float] = (0.85, 1.15),
        retryable_errors: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError, ServerLagException),
    ):
        self.max_attempts = max_respawn_attempts
        self.base_cooldown = base_cooldown
        self.multiplier = multiplier
        self.jitter_bounds = jitter_bounds
        self.retryable_errors = retryable_errors

    def execute_with_retry(self, operation: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Executes operation with ping jitter and retry backoff."""
        delay = self.base_cooldown
        for attempt in range(1, self.max_attempts + 1):
            try:
                return operation(*args, **kwargs)
            except self.retryable_errors as error:
                if attempt == self.max_attempts:
                    raise ServerLagException(
                        f"Matchmaker packet dropped after {attempt} attempts: {error}"
                    ) from error
                
                ping_jitter = random.uniform(*self.jitter_bounds)
                time.sleep(delay * ping_jitter)
                delay *= self.multiplier


def retry_game_packet(attempts: int = 4, initial_delay: float = 0.1):
    """Decorator for auto-retrying fragile matchmaker or telemetry network calls."""
    handler = NetworkRetryHandler(max_respawn_attempts=attempts, base_cooldown=initial_delay)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return handler.execute_with_retry(func, *args, **kwargs)
        return wrapper
    return decorator
