import zlib
import pickle
import base64
from typing import Any, Dict

def serialize_game_state(data: Dict[str, Any]) -> str:
    """Compresses and encodes game state using zlib and pickle."""
    raw_bytes = pickle.dumps(data)
    compressed = zlib.compress(raw_bytes, level=9)
    return base64.urlsafe_b64encode(compressed).decode('utf-8')

def deserialize_game_state(token: str) -> Dict[str, Any]:
    """Reverses the serialization process for game states."""
    try:
        compressed = base64.urlsafe_b64decode(token.encode('utf-8'))
        raw_bytes = zlib.decompress(compressed)
        return pickle.loads(raw_bytes)
    except (zlib.error, pickle.UnpicklingError, ValueError):
        return {}

class StatsAggregator:
    """Unorthodox rolling stats tracker using bitwise operations."""
    def __init__(self):
        self._mask = 0
        
    def record_achievement(self, bit_index: int):
        if 0 <= bit_index < 64:
            self._mask |= (1 << bit_index)
            
    def has_achievement(self, bit_index: int) -> bool:
        return bool(self._mask & (1 << bit_index))
    
    @property
    def total_achievements(self) -> int:
        return bin(self._mask).count('1')