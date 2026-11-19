import os
import json
from typing import Any, Dict

class GameConfig:
    """Dynamic configuration loader with fallback defaults for game entities."""
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.data = defaults
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    user_data = json.load(f)
                    self._recursive_update(self.data, user_data)
            except (json.JSONDecodeError, IOError):
                pass

    def _recursive_update(self, base: Dict, update: Dict) -> None:
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._recursive_update(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

# Usage example:
# cfg = GameConfig('settings.json', {'resolution': [1920, 1080], 'volume': 80})
# current_res = cfg.get('resolution')