import os
import json
from collections import ChainMap
from typing import Any, Dict

class ConfigField:
    def __init__(self, default: Any, type_cast: type):
        self.default = default
        self.type_cast = type_cast

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = instance._resolved.get(self.name, self.default)
        try:
            return self.type_cast(val)
        except (ValueError, TypeError):
            return self.default

class GameConfig:
    """Dynamic configuration loader with profiles for gaming workloads."""

    PRESETS = {
        "potato": {"fps_limit": 30, "fov": 70, "ray_tracing": False, "texture_quality": "low"},
        "esports": {"fps_limit": 360, "fov": 103, "ray_tracing": False, "texture_quality": "medium"},
        "ultra": {"fps_limit": 144, "fov": 90, "ray_tracing": True, "texture_quality": "ultra"}
    }

    fps_limit = ConfigField(60, int)
    fov = ConfigField(90, int)
    ray_tracing = ConfigField(False, lambda x: str(x).lower() in ("true", "1", "yes"))
    texture_quality = ConfigField("medium", str)

    def __init__(self, preset: str = "esports", overrides: Dict[str, Any] = None):
        self.preset = preset if preset in self.PRESETS else "esports"
        self._overrides = overrides or {}
        self._resolved = ChainMap(
            self._overrides,
            self._get_env_overrides(),
            self.PRESETS[self.preset]
        )

    def _get_env_overrides(self) -> Dict[str, Any]:
        prefix = "GAME_"
        return {
            key[len(prefix):].lower(): val
            for key, val in os.environ.items()
            if key.startswith(prefix)
        }

    def load_json(self, json_str: str) -> None:
        try:
            data = json.loads(json_str)
            self._overrides.update(data)
        except json.JSONDecodeError:
            pass
