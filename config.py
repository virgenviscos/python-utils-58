import json
from typing import Any, Dict, Optional

class GameConfig:
    DEFAULTS: Dict[str, Any] = {
        "window": {
            "width": 1024,
            "height": 768,
            "title": "Epic Game"
        },
        "player": {
            "speed": 5.0,
            "health": 100,
            "jump_height": 10
        },
        "game": {
            "max_level": 10,
            "difficulty": "medium",
            "enable_sound": True
        }
    }

    def __init__(self, config_file: Optional[str] = None) -> None:
        self._config: Dict[str, Any] = self._deepcopy(self.DEFAULTS)
        if config_file:
            self.load(config_file)

    def _deepcopy(self, d: Dict[str, Any]) -> Dict[str, Any]:
        return {k: self._deepcopy(v) if isinstance(v, dict) else v for k, v in d.items()}

    def load(self, config_file: str) -> None:
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                loaded_config = json.load(f)
            self._merge_configs(self._config, loaded_config)
        except (FileNotFoundError, json.JSONDecodeError, IOError):
            pass

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value

    def get(self, path: str, default: Any = None) -> Any:
        keys = path.split(".")
        current = self._config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def set(self, path: str, value: Any) -> None:
        keys = path.split(".")
        current = self._config
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        return self._deepcopy(self._config)

    def save(self, config_file: str) -> None:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2)