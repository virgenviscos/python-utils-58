import json
import os

class ConfigLoader:
    def __init__(self, default_config_file):
        self.default_config_file = default_config_file
        self.config = self.load_defaults()

    def load_defaults(self):
        with open(self.default_config_file, 'r') as file:
            return json.load(file)

    def load_user_config(self, user_config_file):
        if os.path.exists(user_config_file):
            with open(user_config_file, 'r') as file:
                user_config = json.load(file)
            self.config.update(user_config)

    def get(self, key, default=None):
        return self.config.get(key, default)

if __name__ == '__main__':
    loader = ConfigLoader('default_config.json')
    loader.load_user_config('user_config.json')
    print(loader.get('some_key', 'default_value'))