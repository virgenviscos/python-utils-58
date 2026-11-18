from typing import Dict, List, Any, Optional, Callable

class GameEventDispatcher:
    """Manages callback registration for specific game-world triggers."""

    def __init__(self) -> None:
        self._callbacks: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """Adds a listener for a particular event identifier."""
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []
        self._callbacks[event_type].append(callback)

    def trigger(self, event_type: str, data: Optional[Any] = None) -> None:
        """Executes all registered callbacks for the given event type."""
        for callback in self._callbacks.get(event_type, []):
            try:
                callback(data)
            except Exception as e:
                print(f"[Error] Execution failure in {callback.__name__}: {e}")

    def __repr__(self) -> str:
        """Displays total registered event channels."""
        return f"<GameEventDispatcher channels={len(self._callbacks)} >"

def sync_handler(data: Dict[str, Any]) -> None:
    """Utility for logging payload throughput."""
    print(f"Processing entity update: {data.get('id', 'unknown')}")