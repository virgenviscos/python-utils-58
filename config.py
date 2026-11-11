import os
import json
from collections import ChainMap
from typing import Any, Dict, Union

DEFAULT_GAME_CONFIG: Dict[str, Any] = {
    "display.width": 1920,
    "display.height": 1080,
    "display.fullscreen": True,
    "graphics.fov": 90.0,
    "graphics.fps_limit": 144,
    "graphics.preset": "ultra",
    "audio.master": 0.8,
    "audio.sfx": 1.0,
    "audio.music": 0.5,
    "gameplay.difficulty": "normal",
    "gameplay.invert_y": False,
}

class GameConfigLoader:
    """Dynamic gaming configuration proxy with environment override mapping."""

    def __init__(self, filepath: Union[str, None] = None) -> None:
        self._file_defaults = self._load_file(filepath) if filepath else {}
        self._env_overrides = self._parse_env()
        self._storage = ChainMap(self._env_overrides, self._file_defaults, DEFAULT_GAME_CONFIG)

    def _load_file(self, filepath: str) -> Dict[str, Any]:
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _parse_env(self) -> Dict[str, Any]:
        overrides = {}
        prefix = "GAME_CFG_"
        for key, val in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower().replace("__", ".")
                overrides[clean_key] = self._cast_val(clean_key, val)
        return overrides

    def _cast_val(self, key: str, raw_val: str) -> Any:
        default_val = DEFAULT_GAME_CONFIG.get(key)
        if isinstance(default_val, bool):
            return raw_val.lower() in ("true", "1", "yes")
        if isinstance(default_val, int):
            return int(raw_val)
        if isinstance(default_val, float):
            return float(raw_val)
        return raw_val

    def get(self, key: str) -> Any:
        return self._storage.get(key)

    def __getattr__(self, name: str) -> Any:
        dot_key = name.replace("_", ".")
        if dot_key in self._storage:
            return self._storage[dot_key]
        raise AttributeError(f"Configuration key '{name}' (or '{dot_key}') not found")

    def dump_active(self) -> Dict[str, Any]:
        return dict(self._storage)
