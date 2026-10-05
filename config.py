import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic config loader with magic attribute access."""
    def __init__(self, file_path: str, defaults: Dict[str, Any] = None):
        self._data = defaults or {}
        self.file_path = file_path
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try:
                    self._data.update(json.load(f))
                except json.JSONDecodeError:
                    pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config key {name} not found')

    def save(self) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def update(self, **kwargs) -> None:
        self._data.update(kwargs)

DEFAULT_GAME_CONFIG = {
    'resolution': [1920, 1080],
    'volume': 0.8,
    'vsync': True,
    'player_name': 'unnamed_warrior'
}

settings = ConfigLoader('settings.json', DEFAULT_GAME_CONFIG)