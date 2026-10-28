import functools
from typing import Callable, Any, Dict, List, Tuple


class StatusMask(int):
    """Bitwise state container with dynamic attribute lookup for game status conditions."""

    def __getattr__(self, status_name: str) -> bool:
        bit_index = sum(ord(char) for char in status_name.lower()) % 64
        return bool((self >> bit_index) & 1)

    def set_status(self, status_name: str, active: bool = True) -> "StatusMask":
        bit_index = sum(ord(char) for char in status_name.lower()) % 64
        if active:
            return StatusMask(self | (1 << bit_index))
        return StatusMask(self & ~(1 << bit_index))


class DynamicGameHandler:
    """Reactive event processor managing game entity callbacks and state transformations."""

    def __init__(self):
        self._events: Dict[str, List[Callable]] = {}
        self.status = StatusMask(0)

    def bind(self, event_name: str):
        """Decorator to attach listener functions to a game event."""
        def decorator(fn: Callable) -> Callable:
            self._events.setdefault(event_name, []).append(fn)
            return fn
        return decorator

    def emit(self, event_name: str, *args, **kwargs) -> List[Any]:
        """Trigger all listeners for a given event, collecting their return values."""
        return [fn(*args, **kwargs) for fn in self._events.get(event_name, [])]

    def apply_effect(self, entity_id: str, effect_name: str) -> Tuple[StatusMask, List[Any]]:
        """Applies status effect to mask and dispatches effect payload."""
        self.status = self.status.set_status(effect_name, True)
        outcomes = self.emit(f"effect:{effect_name}", entity_id, self.status)
        return self.status, outcomes
