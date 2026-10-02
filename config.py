import json
import os
from collections import ChainMap
from typing import Any, Dict, Optional

DEFAULT_GAMING_CONFIG: Dict[str, Any] = {
    "graphics.fps_limit": 144,
    "graphics.vsync": True,
    "graphics.resolution": "1920x1080",
    "audio.master_volume": 0.8,
    "audio.mute_on_focus_loss": True,
    "gameplay.difficulty": "hardcore",
    "gameplay.fov": 90,
    "controls.invert_y": False,
    "network.server_port": 27015,
}

class GameConfig:
    """Dynamic dot-notation configuration manager with fallback layers."""

    def __init__(self, config_path: Optional[str] = None, **overrides: Any):
        file_cfg = self._load_file(config_path) if config_path else {}
        env_cfg = self._load_env()
        self._store = ChainMap(overrides, env_cfg, file_cfg, DEFAULT_GAMING_CONFIG)

    def _load_file(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_env(self) -> Dict[str, Any]:
        prefix = "GAME_CFG_"
        env_data = {}
        for key, val in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower().replace("__", ".")
                env_data[clean_key] = self._parse_val(val)
        return env_data

    @staticmethod
    def _parse_val(val: str) -> Any:
        if val.lower() in ("true", "false"):
            return val.lower() == "true"
        try:
            return int(val) if val.isdigit() else float(val)
        except ValueError:
            return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def __getattr__(self, name: str) -> Any:
        key = name.replace("_", ".")
        if key in self._store:
            return self._store[key]
        raise AttributeError(f"Configuration key '{name}' not found")

    def dump(self) -> Dict[str, Any]:
        return dict(self._store)
