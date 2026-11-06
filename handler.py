import zlib
import pickle
import base64
from typing import Any, Dict

class GameStateSerializer:
    def __init__(self, secret_salt: str = 'G4M3R_PR0'):
        self.salt = secret_salt.encode()

    def pack(self, data: Dict[str, Any]) -> str:
        raw = pickle.dumps(data)
        compressed = zlib.compress(raw + self.salt, level=9)
        return base64.urlsafe_b64encode(compressed).decode('utf-8')

    def unpack(self, payload: str) -> Dict[str, Any]:
        try:
            raw = base64.urlsafe_b64decode(payload)
            decompressed = zlib.decompress(raw)
            if not decompressed.endswith(self.salt):
                raise ValueError('tampered save file detected')
            return pickle.loads(decompressed[:-len(self.salt)])
        except (zlib.error, pickle.UnpicklingError, ValueError) as e:
            return {'error': 'corrupted_state', 'details': str(e)}

def extract_player_stats(payload: str) -> Dict[str, Any]:
    handler = GameStateSerializer()
    state = handler.unpack(payload)
    stats = state.get('stats', {})
    return {k: v for k, v in stats.items() if isinstance(v, (int, float))}

if __name__ == '__main__':
    packer = GameStateSerializer()
    test_data = {'stats': {'hp': 100, 'xp': 550, 'mana': 80}, 'pos': (10, 20)}
    encoded = packer.pack(test_data)
    print(f'serialized state length: {len(encoded)}')
    print(f'extracted stats: {extract_player_stats(encoded)}')