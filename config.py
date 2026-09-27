import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with fallback strategy."""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}
        self._filepath = Path("settings.json")

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def load(self) -> None:
        try:
            if self._filepath.exists():
                with open(self._filepath, "r") as f:
                    loaded = json.load(f)
                    self._data.update({k: v for k, v in loaded.items() if v is not None})
        except (json.JSONDecodeError, IOError):
            pass

    def persist(self) -> None:
        with open(self._filepath, "w") as f:
            json.dump(self._data, f, indent=4)

    def patch(self, updates: Dict[str, Any]) -> None:
        self._data.update(updates)

def get_game_config() -> ConfigLoader:
    defaults = {
        "resolution": [1920, 1080],
        "vsync": True,
        "fov": 90,
        "volume": 0.8
    }
    instance = ConfigLoader(defaults)
    instance.load()
    return instance