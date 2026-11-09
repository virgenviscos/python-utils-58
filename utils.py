import zlib
import base64
import json
from typing import Any, Dict

def pack_game_state(state_dict: Dict[str, Any]) -> str:
    """Compresses game state into a compact web-safe string."""
    json_data = json.dumps(state_dict, separators=(',', ':'))
    compressed = zlib.compress(json_data.encode('utf-8'), level=9)
    return base64.urlsafe_b64encode(compressed).decode('utf-8')

def unpack_game_state(payload: str) -> Dict[str, Any]:
    """Inflates compact game state back into python dictionary."""
    raw = base64.urlsafe_b64decode(payload)
    decompressed = zlib.decompress(raw)
    return json.loads(decompressed.decode('utf-8'))

class DataEnvelope:
    def __init__(self, raw_data: Any):
        self.payload = raw_data
        self.version = 58

    def serialize(self) -> str:
        return pack_game_state({
            'v': self.version,
            'data': self.payload
        })

if __name__ == '__main__':
    envelope = DataEnvelope({'player': 'hero', 'hp': 100, 'items': ['sword', 'shield']})
    blob = envelope.serialize()
    print(f'Compressed state: {blob}')
    print(f'Decoded: {unpack_game_state(blob)}')