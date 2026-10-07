import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Magic configuration injector with fallback logic."""
    def __init__(self, defaults: Dict[str, Any], path: str = 'settings.json'):
        self.path = path
        self.data = defaults
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    loaded = json.load(f)
                    self.data.update({k: v for k, v in loaded.items() if k in self.data})
            except (json.JSONDecodeError, IOError):
                pass

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

def get_game_config():
    defaults = {
        "resolution": [1920, 1080],
        "vsync": True,
        "master_volume": 0.8,
        "keybinds": {"jump": "space", "crouch": "ctrl"}
    }
    return ConfigLoader(defaults)