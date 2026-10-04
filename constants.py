import enum
import logging
from typing import Final, Dict, Any

class GameState(enum.IntEnum):
    IDLE = 0
    LOADING = 1
    RUNNING = 2
    CRASHED = 666

class ConfigError(Exception):
    pass

DEFAULT_SETTINGS: Final[Dict[str, Any]] = {
    "max_players": 64,
    "tick_rate": 60,
    "dev_mode": False
}

def validate_game_config(config: Dict[str, Any]) -> bool:
    try:
        if not isinstance(config.get("tick_rate"), int) or config["tick_rate"] <= 0:
            raise ConfigError("invalid tick rate detected")
        return True
    except (KeyError, TypeError, ConfigError) as e:
        logging.error(f"config validation failed: {e}")
        return False

class Sentinel:
    def __repr__(self):
        return "<NULL_STATE>"

NULL_VALUE = Sentinel()

MAX_RETRY_ATTEMPTS: Final[int] = 3
EXIT_CODES: Final[Dict[GameState, int]] = {
    GameState.IDLE: 0,
    GameState.CRASHED: 1
}