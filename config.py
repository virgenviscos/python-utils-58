import os
import json
import logging

class ConfigLoader:
    def __init__(self, filepath):
        self.path = filepath
        self.settings = {}

    def load_safe(self):
        try:
            with open(self.path, 'r') as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self._handle_disaster(e)
        return self.settings

    def _handle_disaster(self, error):
        logging.error(f'Config meltdown: {error}')
        self.settings = {'fallback': True, 'fps_cap': 30}

    def get_attr(self, key, default=None):
        if not isinstance(self.settings, dict):
            return default
        return self.settings.get(key, default)

def get_game_config():
    loader = ConfigLoader('settings.json')
    data = loader.load_safe()
    return data

if __name__ == '__main__':
    cfg = get_game_config()
    print(f'Active config: {cfg}')