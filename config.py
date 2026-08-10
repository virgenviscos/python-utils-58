import json
import os
from typing import Any, Dict 

class ConfigLoader:
    def __init__(self, default_config: Dict[str, Any], config_file: str = 'config.json'):
        self.default_config = default_config
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                user_config = json.load(file)
                return self.merge_configs(self.default_config, user_config)
        return self.default_config

    def merge_configs(self, defaults: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        merged = defaults.copy()
        merged.update(user)
        return merged

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

# Example default configuration
DEFAULTS = {
    'host': 'localhost',
    'port': 8080,
    'debug': False
}

# Usage
if __name__ == '__main__':
    config_loader = ConfigLoader(DEFAULTS)
    print(config_loader.get('host'))
    print(config_loader.get('port'))
    print(config_loader.get('missing_key', 'default_value'))