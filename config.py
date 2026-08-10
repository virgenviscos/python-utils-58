import json
import os

class ConfigLoader:
    def __init__(self, default_config, user_config_path='config.json'):
        self.default_config = default_config
        self.user_config_path = user_config_path
        self.config = self.load_config()

    def load_config(self):
        config = self.default_config.copy()
        if os.path.exists(self.user_config_path):
            with open(self.user_config_path, 'r') as user_config_file:
                user_config = json.load(user_config_file)
                config.update(user_config)
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        with open(self.user_config_path, 'w') as user_config_file:
            json.dump(self.config, user_config_file)

# Example default configuration
DEFAULT_CONFIG = {
    'setting1': 'value1',
    'setting2': 'value2',
    'setting3': 10
}

# Usage:
# config_loader = ConfigLoader(DEFAULT_CONFIG)
# print(config_loader.get('setting1'))
# config_loader.set('setting4', 'value4')
