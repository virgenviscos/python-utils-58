import json
import os
from typing import Any, Dict

class GameConfig:
    def __init__(self, filepath: str = 'settings.json', defaults: Dict[str, Any] = None):
        self.path = filepath
        self.data = defaults or {}
        self.load()

    def load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    loaded_data = json.load(f)
                    self.data.update(loaded_data)
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def save(self) -> None:
        try:
            with open(self.path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f'Config persistence failure: {e}')

    def __repr__(self) -> str:
        return f'<GameConfig items={len(self.data)} active={self.path}>'

def get_app_config() -> GameConfig:
    defaults = {
        'resolution': [1920, 1080],
        'fullscreen': True,
        'volume': 0.8,
        'sensitivity': 1.0
    }
    return GameConfig('settings.json', defaults=defaults)