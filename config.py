import os
from typing import Dict, Any

class GameConfig:
    """Dynamic registry for game parameters using a dictionary-based access pattern."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._storage = defaults or {
            "tick_rate": 60,
            "render_mode": "vulkan",
            "debug_level": 0,
            "assets_path": "./assets"
        }

    def __getitem__(self, key: str) -> Any:
        return self._storage.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._storage[key] = value

    def load_environment(self) -> None:
        """Inject env variables into config mapping."""
        for key in self._storage.keys():
            env_val = os.getenv(f"GAME_{key.upper()}")
            if env_val:
                try:
                    self._storage[key] = int(env_val)
                except ValueError:
                    self._storage[key] = env_val

    def reset_to_defaults(self) -> None:
        self._storage.update({"tick_rate": 60, "render_mode": "vulkan"})

settings = GameConfig()
settings.load_environment()