import functools
import time
from typing import Callable, Any

class GameStateRegistry:
    def __init__(self):
        self._data = {}
        self._hooks = []

    def __setitem__(self, key: str, value: Any):
        self._data[key] = value
        for hook in self._hooks:
            hook(key, value)

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def attach(self, callback: Callable[[str, Any], None]):
        self._hooks.append(callback)

def throttle(interval: float):
    def decorator(func):
        last_called = 0.0
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            elapsed = time.time() - last_called
            if elapsed >= interval:
                last_called = time.time()
                return func(*args, **kwargs)
        return wrapper
    return decorator

class EngineCore:
    def __init__(self):
        self.registry = GameStateRegistry()
        self.running = True

    @throttle(0.016)
    def tick(self, frame_id: int):
        if self.running:
            self.registry['frame'] = frame_id

    def shutdown(self):
        self.running = False
        print("System state synchronized and finalized")

if __name__ == '__main__':
    engine = EngineCore()
    engine.registry.attach(lambda k, v: print(f"State Update: {k}={v}"))
    for i in range(5):
        engine.tick(i)