import os
from typing import Any, Dict, get_type_hints

class GameConfig:
    """
    Self-healing dynamic configuration manager for retro game engines.
    Uses type hints to auto-cast environment variables with smart defaults.
    """
    # Game Defaults
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    MAX_FPS: int = 60
    SOUND_VOLUME: float = 0.8
    DEBUG_MODE: bool = False
    GAME_TITLE: str = "Retro Starfighter"

    def __init__(self) -> None:
        self._cache: Dict[str, Any] = {}
        self._load_environment_overrides()

    def _load_environment_overrides(self) -> None:
        hints = get_type_hints(self.__class__)
        for key, expected_type in hints.items():
            env_val = os.getenv(f"GAME_{key}")
            if env_val is not None:
                try:
                    self._cache[key] = self._cast_value(env_val, expected_type)
                except (ValueError, TypeError):
                    pass

    def _cast_value(self, value: str, target_type: Any) -> Any:
        if target_type is bool:
            return value.lower() in ("true", "1", "yes", "on")
        return target_type(value)

    def __getattr__(self, name: str) -> Any:
        if name in self._cache:
            return self._cache[name]
        if hasattr(self.__class__, name):
            return getattr(self.__class__, name)
        raise AttributeError(f"Configuration parameter '{name}' not found.")

    def update_setting(self, name: str, value: Any) -> None:
        hints = get_type_hints(self.__class__)
        if name not in hints:
            raise ValueError(f"Invalid configuration key: {name}")
        target_type = hints[name]
        try:
            if target_type is bool and isinstance(value, str):
                self._cache[name] = self._cast_value(value, bool)
            else:
                self._cache[name] = target_type(value)
        except (ValueError, TypeError) as err:
            raise TypeError(f"Cannot cast {value} to {target_type}") from err

    def reset_to_defaults(self) -> None:
        self._cache.clear()