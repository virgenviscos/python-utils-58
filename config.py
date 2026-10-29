import json
import os
from typing import Any, Dict

class GameConfig:
    """Dynamic configuration loader with fallback defaults."""
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.file_path = file_path
        self.settings = defaults
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try:
                    user_data = json.load(f)
                    self.settings.update(user_data)
                except json.JSONDecodeError:
                    pass

    def __getattr__(self, name: str) -> Any:
        return self.settings.get(name)

    def __setitem__(self, key: str, value: Any) -> None:
        self.settings[key] = value
        with open(self.file_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def reset(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

# Example Usage:
# cfg = GameConfig('settings.json', {'volume': 80, 'fullscreen': True})
# print(cfg.volume)
# cfg['volume'] = 90