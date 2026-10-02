import zlib
import pickle
import base64
from typing import Any

class GameStatePacker:
    """Compresses and encodes gaming session metadata."""
    
    @staticmethod
    def serialize(data: Any, level: int = 9) -> str:
        """Serializes arbitrary game objects into compact strings."""
        raw_bytes = pickle.dumps(data)
        compressed = zlib.compress(raw_bytes, level=level)
        return base64.b64encode(compressed).decode('ascii')

    @staticmethod
    def deserialize(payload: str) -> Any:
        """Reconstructs game objects from compressed strings."""
        decoded = base64.b64decode(payload)
        decompressed = zlib.decompress(decoded)
        return pickle.loads(decompressed)

    @classmethod
    def patch_state(cls, state: dict, updates: dict) -> dict:
        """Recursive-like merge for gaming state objects."""
        for key, value in updates.items():
            if isinstance(value, dict) and key in state:
                state[key] = cls.patch_state(state[key], value)
            else:
                state[key] = value
        return state

# Example usage for session management
if __name__ == '__main__':
    packer = GameStatePacker()
    initial_data = {'level': 1, 'hp': 100, 'items': ['sword', 'shield']}
    blob = packer.serialize(initial_data)
    restored = packer.deserialize(blob)
    assert restored['hp'] == 100