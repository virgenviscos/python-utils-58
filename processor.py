import functools
from typing import Any, Callable, Dict

class GameStateProcessor:
    def __init__(self, state: Dict[str, Any]):
        self._state = state
        self._hooks = []

    def register_hook(self, func: Callable[[Dict], Dict]) -> None:
        self._hooks.append(func)

    def process_frame(self) -> Dict[str, Any]:
        return functools.reduce(
            lambda s, hook: hook(s),
            self._hooks,
            self._state
        )

def health_clamp(state: Dict[str, Any]) -> Dict[str, Any]:
    state['health'] = max(0, min(100, state.get('health', 0)))
    return state

def xp_multiplier(state: Dict[str, Any]) -> Dict[str, Any]:
    state['xp'] = int(state.get('xp', 0) * 1.05)
    return state

def run_pipeline(initial_data: Dict[str, Any]) -> Dict[str, Any]:
    processor = GameStateProcessor(initial_data)
    processor.register_hook(health_clamp)
    processor.register_hook(xp_multiplier)
    return processor.process_frame()