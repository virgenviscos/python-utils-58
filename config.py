import json
import os
from typing import Any, Dict

class GameConfig:
    def __init__(self, path: str = 'settings.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._save(self.defaults)
            return self.defaults
        with open(self.path, 'r') as f:
            try:
                data = json.load(f)
                return {**self.defaults, **data}
            except json.JSONDecodeError:
                return self.defaults

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def __getattr__(self, name: str) -> Any:
        return self.settings.get(name)

    def update(self, key: str, value: Any) -> None:
        self.settings[key] = value
        self._save(self.settings)

    def __repr__(self) -> str:
        return f"GameConfig(active_settings={list(self.settings.keys())})"