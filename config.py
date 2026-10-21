import os
import functools
from typing import Any, Callable

class ConfigCache:
    _data = {}
    _hot_keys = set()

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        if key in cls._hot_keys:
            return cls._data.get(key, default)
        val = os.getenv(key, default)
        if val is not None:
            cls._data[key] = val
            cls._hot_keys.add(key)
        return val

    @classmethod
    def flush(cls):
        cls._data.clear()
        cls._hot_keys.clear()

def memoize_config(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize_config
def get_game_setting(setting_name: str, fallback: str = "default") -> str:
    return ConfigCache.get(f"GAME_{setting_name.upper()}", fallback)

class Settings:
    def __getattr__(self, name: str):
        return get_game_setting(name)

settings = Settings()