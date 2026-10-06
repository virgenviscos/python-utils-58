import functools
import sys

class GameConfig:
    __slots__ = ('_settings', '_cache')

    def __init__(self):
        self._settings = {}
        self._cache = {}

    @functools.lru_cache(maxsize=128)
    def get_setting(self, key: str):
        return self._settings.get(key)

    def set_setting(self, key: str, value):
        self._settings[key] = value
        self.get_setting.cache_clear()

    def batch_update(self, updates: dict):
        self._settings.update(updates)
        self.get_setting.cache_clear()

    def __getitem__(self, key):
        val = self.get_setting(key)
        if val is None:
            raise KeyError(f'Configuration key {key} missing')
        return val

    def __setitem__(self, key, value):
        self.set_setting(key, value)

    def __delitem__(self, key):
        if key in self._settings:
            del self._settings[key]
            self.get_setting.cache_clear()

    def memory_footprint(self):
        return sys.getsizeof(self._settings) + sys.getsizeof(self._cache)

# Global instance for high-speed game state access
config_registry = GameConfig()