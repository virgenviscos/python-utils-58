import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic attribute-based configuration loader for game settings."""
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self._path = file_path
        self._data = defaults.copy()
        self._load()

    def _load(self) -> None:
        if os.path.exists(self._path):
            with open(self._path, 'r') as f:
                try:
                    self._data.update(json.load(f))
                except json.JSONDecodeError:
                    pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Key '{name}' not found in configuration")

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def save(self) -> None:
        with open(self._path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def update(self, key: str, value: Any) -> None:
        self._data[key] = value

def get_game_config(path: str = "settings.json") -> ConfigLoader:
    defaults = {
        "resolution": [1920, 1080],
        "vsync": True,
        "master_volume": 0.8,
        "player_name": "Hero"
    }
    return ConfigLoader(path, defaults)