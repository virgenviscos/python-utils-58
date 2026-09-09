import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.data = defaults
        self._sync()

    def _sync(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                try:
                    user_data = json.load(f)
                    self.data.update(user_data)
                except json.JSONDecodeError:
                    pass
        else:
            self.save()

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self) -> str:
        return f"<ConfigLoader loaded={list(self.data.keys())}>"