import functools
import time
from typing import Any, Callable, Dict, List, Generator


class GameProcessorPipeline:
    """Dynamic game frame processor with automatic stale state purge."""

    def __init__(self, ttl_seconds: float = 5.0) -> None:
        self._ttl: float = ttl_seconds
        self._registry: Dict[str, List[Callable[[Dict[str, Any]], Dict[str, Any]]]] = {}
        self._state_history: List[Dict[str, Any]] = []

    def register(self, event_type: str) -> Callable:
        """Decorator registering handlers into reorganized channels."""
        def decorator(func: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Callable:
            self._registry.setdefault(event_type, []).append(func)
            @functools.wraps(func)
            def wrapper(data: Dict[str, Any]) -> Dict[str, Any]:
                data["_processed_at"] = time.time()
                return func(data)
            return wrapper
        return decorator

    def __call__(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute processing pipeline for a given gaming event."""
        handlers = self._registry.get(event_type, [])
        current = payload.copy()
        current["_processed_at"] = time.time()
        for handler in handlers:
            current = handler(current)
        self._state_history.append(current)
        self._purge_stale_records()
        return current

    def _purge_stale_records(self) -> None:
        """Unusual inline list filtering to clean up expired frame history."""
        now = time.time()
        self._state_history[:] = [
            entry for entry in self._state_history
            if now - entry.get("_processed_at", now) < self._ttl
        ]

    def stream_events(self, raw_events: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        """Generator yielding sanitized gaming frame state updates."""
        for evt in raw_events:
            etype = evt.get("type", "generic")
            yield self(etype, evt)


frame_processor = GameProcessorPipeline(ttl_seconds=3.0)