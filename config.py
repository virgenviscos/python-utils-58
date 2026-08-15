import json
import os

class ConfigLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.user_config = {}

    def load_config(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as config_file:
                self.user_config = json.load(config_file)
        else:
            print(f'No config file found at {file_path}, using defaults.')

    def get_config(self):
        combined_config = self.default_config.copy()
        combined_config.update(self.user_config)
        return combined_config

# Example of usage
if __name__ == '__main__':
    default_settings = {
        'resolution': '1920x1080',
        'fullscreen': True,
        'volume': 75,
        'controls': {'move_up': 'W', 'move_down': 'S', 'move_left': 'A', 'move_right': 'D'}
    }
    loader = ConfigLoader(default_settings)
    loader.load_config('user_config.json')
    final_config = loader.get_config()
    print(final_config)