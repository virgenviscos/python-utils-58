import time
import collections
from typing import Dict, Any, Callable

class GameEventHandler:
    def __init__(self):
        self._registry: Dict[str, list] = collections.defaultdict(list)
        self._tick_rate = 0.016

    def register(self, event_type: str, callback: Callable):
        self._registry[event_type].append(callback)
        return self

    def emit(self, event_type: str, data: Any = None):
        for callback in self._registry.get(event_type, []):
            try:
                callback(data)
            except Exception as e:
                print(f"fault in {event_type} sequence: {e}")

    def process_queue(self, queue: list):
        start = time.perf_counter()
        while queue:
            evt = queue.pop(0)
            self.emit(evt.get('type'), evt.get('payload'))
            if time.perf_counter() - start > self._tick_rate:
                break

class EntityStreamProcessor:
    def __init__(self):
        self.state = {}

    def sanitize(self, raw_data: Dict[str, Any]):
        return {k: v for k, v in raw_data.items() if v is not None}

    def sync_state(self, entity_id: str, patch: Dict[str, Any]):
        current = self.state.get(entity_id, {})
        current.update(self.sanitize(patch))
        self.state[entity_id] = current
        return current