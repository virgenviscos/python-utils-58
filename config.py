import os
import logging
from typing import Any, Dict

class ConfigError(Exception):
    """Custom catastrophe for malformed gaming configuration."""
    pass

def load_game_config(filepath: str) -> Dict[str, Any]:
    config_data = {}
    if not os.path.exists(filepath):
        raise ConfigError(f"Missing game assets at {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if '#' in line: line = line.split('#')[0]
                if '=' not in line: continue
                key, val = map(str.strip, line.split('=', 1))
                config_data[key] = val
        
        if not config_data:
            raise ValueError("Empty config detected")
            
    except (IOError, ValueError) as e:
        logging.error(f"Config corruption detected: {e}")
        return {"default_fps": "60", "mode": "safe_mode"}
        
    return config_data

class ConfigSanitizer:
    def __init__(self, settings: Dict[str, str]):
        self.settings = settings

    def get_int(self, key: str, fallback: int) -> int:
        try:
            return int(self.settings.get(key, fallback))
        except (TypeError, ValueError):
            return fallback