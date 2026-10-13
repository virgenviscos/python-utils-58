import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.config = defaults
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                try:
                    user_data = json.load(f)
                    self._recursive_update(self.config, user_data)
                except json.JSONDecodeError:
                    pass

    def _recursive_update(self, base: Dict, patch: Dict) -> None:
        for key, value in patch.items():
            if isinstance(value, dict) and key in base:
                self._recursive_update(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

def load_game_config(path: str) -> ConfigLoader:
    defaults = {
        'graphics': {'resolution': '1920x1080', 'vsync': True},
        'audio': {'master': 80, 'music': 50},
        'gameplay': {'difficulty': 'normal'}
    }
    return ConfigLoader(path, defaults)