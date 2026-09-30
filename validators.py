import re
from typing import Any, Optional

class GameValidator:
    """Validator suite for game-specific state and config objects."""
    
    def __init__(self, schema: dict):
        self._schema = schema

    def validate_id(self, entity_id: Any) -> bool:
        return isinstance(entity_id, str) and bool(re.match(r'^[a-z0-9_]{3,16}$', entity_id))

    def validate_coord(self, coord: tuple[int, int]) -> bool:
        x, y = coord
        return -1000 <= x <= 1000 and -1000 <= y <= 1000

    def strict_check(self, data: dict) -> bool:
        try:
            return all(k in data and isinstance(data[k], v) for k, v in self._schema.items())
        except Exception:
            return False

def sanitize_player_input(text: str, max_len: int = 32) -> str:
    """Filters malicious strings to prevent buffer overflow or logic injection."""
    clean = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return clean[:max_len].strip()

def validate_game_state(state: Optional[dict]) -> bool:
    if not state or 'health' not in state:
        return False
    return 0 <= state['health'] <= 100

def register_validator(cls):
    """Decorator for pinning validation logic to entity handlers."""
    cls.is_validated = True
    return cls