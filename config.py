import json
import os
from typing import Any, Dict

class GameConfig:
    """Dynamic configuration loader using attribute magic."""
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self._path = path
        self._data = defaults.copy()
        self._load_file()

    def _load_file(self) -> None:
        if os.path.exists(self._path):
            with open(self._path, 'r') as f:
                self._data.update(json.load(f))

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def save(self) -> None:
        with open(self._path, 'w') as f:
            json.dump(self._data, f, indent=4)

def get_config(filename: str = 'settings.json') -> GameConfig:
    defaults = {
        "resolution": "1920x1080",
        "vsync": True,
        "fov": 90,
        "volume": 0.8
    }
    return GameConfig(filename, defaults)