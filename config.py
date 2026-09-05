import json
from pathlib import Path
from typing import Any, Dict, Union

class ConfigProxy(dict):
    """Hierarchical config proxy supporting default fallbacks and attribute access."""
    
    def __init__(self, defaults: Dict[str, Any], data: Dict[str, Any] = None):
        super().__init__()
        self._defaults = defaults
        if data:
            self.update(data)

    def __getitem__(self, item: str) -> Any:
        val = super().get(item, self._defaults.get(item))
        if val is None and item not in self._defaults and item not in self:
            raise KeyError(f"Setting '{item}' does not exist in configuration.")
        
        default_sub = self._defaults.get(item, {})
        if isinstance(val, dict):
            def_dict = default_sub if isinstance(default_sub, dict) else {}
            return ConfigProxy(def_dict, val)
        return val

    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(e) from None


DEFAULT_GAMING_SETTINGS: Dict[str, Any] = {
    "display": {"width": 1920, "height": 1080, "fov": 90, "vsync": True},
    "audio": {"master_volume": 0.8, "sfx_volume": 1.0, "bgm_volume": 0.6},
    "gameplay": {"difficulty": "hardcore", "auto_save_interval": 300},
    "keybinds": {"primary_attack": "mouse1", "dash": "space", "inventory": "tab"}
}


def load_config(filepath: Union[str, Path] = "config.json") -> ConfigProxy:
    path = Path(filepath)
    user_config = {}
    if path.exists() and path.is_file():
        try:
            with open(path, "r", encoding="utf-8") as file:
                user_config = json.load(file)
        except json.JSONDecodeError:
            pass
    return ConfigProxy(DEFAULT_GAMING_SETTINGS, user_config)
