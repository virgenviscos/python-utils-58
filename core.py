import time
import collections
from typing import Any, Callable, Dict

class GameStateRegistry:
    def __init__(self):
        self._store = collections.defaultdict(dict)
        self._lifecycle_hooks = []

    def register_hook(self, func: Callable[[str], None]):
        self._lifecycle_hooks.append(func)

    def update_state(self, entity_id: str, data: Dict[str, Any]):
        self._store[entity_id].update({**data, "_ts": time.time()})
        for hook in self._lifecycle_hooks:
            hook(entity_id)

    def get_state(self, entity_id: str) -> Dict[str, Any]:
        return self._store.get(entity_id, {})

    def flush(self, timeout: float = 60.0):
        now = time.time()
        expired = [eid for eid, data in self._store.items() if now - data.get("_ts", 0) > timeout]
        for eid in expired:
            del self._store[eid]

def create_engine():
    registry = GameStateRegistry()
    def cleanup_wrapper():
        registry.flush()
    return registry, cleanup_wrapper

if __name__ == "__main__":
    engine, cleanup = create_engine()
    engine.update_state("player_1", {"hp": 100, "pos": (0, 0)})
    cleanup()