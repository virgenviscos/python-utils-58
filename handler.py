import time
from typing import Callable, Any, Dict, List, Tuple


class GamingEventHandler:
    def __init__(self) -> None:
        self._routes: Dict[str, List[Tuple[Callable[..., Any], int]]] = {}
        self._history: List[Tuple[float, str, Dict[str, Any]]] = []

    def register(self, event_type: str, priority: int = 10):
        def decorator(func: Callable[..., Any]):
            if event_type not in self._routes:
                self._routes[event_type] = []
            self._routes[event_type].append((func, priority))
            self._routes[event_type].sort(key=lambda item: item[1], reverse=True)
            return func
        return decorator

    def dispatch(self, event_type: str, **payload: Any) -> List[Any]:
        results = []
        if event_type not in self._routes:
            return results

        timestamp = time.time()
        self._history.append((timestamp, event_type, payload))
        if len(self._history) > 100:
            self._history.pop(0)

        for callback, _ in self._routes[event_type]:
            res = callback(**payload)
            results.append(res)
        return results

    def purge_history_before(self, cutoff_time: float) -> int:
        initial_count = len(self._history)
        self._history = [entry for entry in self._history if entry[0] >= cutoff_time]
        return initial_count - len(self._history)
