import struct
from typing import Tuple, Generator, Dict, Any

class GameTelemetryProcessor:
    """Creative dynamic stream packer for high-frequency spatial game events."""
    
    HEADER_STRUCT = struct.Struct("<IHB")
    
    def __init__(self, precision: int = 2):
        self.scale = 10 ** precision
        self.history: Dict[int, Tuple[int, int, int]] = {}

    def pack_event(self, frame: int, player_id: int, pos: Tuple[float, float, float], flags: int) -> bytes:
        """Packs spatial position and flags into variable delta binary buffer."""
        ix, iy, iz = (int(round(c * self.scale)) for c in pos)
        
        prev = self.history.get(player_id, (ix, iy, iz))
        dx, dy, dz = ix - prev[0], iy - prev[1], iz - prev[2]
        self.history[player_id] = (ix, iy, iz)

        if all(-32768 <= d <= 32767 for d in (dx, dy, dz)):
            header = self.HEADER_STRUCT.pack(frame, player_id, flags | 0x80)
            payload = struct.pack("<hhh", dx, dy, dz)
        else:
            header = self.HEADER_STRUCT.pack(frame, player_id, flags & ~0x80)
            payload = struct.pack("<iii", ix, iy, iz)

        return header + payload

    def process_stream(self, stream: bytes) -> Generator[Dict[str, Any], None, None]:
        """Generator decoding binary telemetry stream into dict frames."""
        offset = 0
        stream_len = len(stream)
        
        while offset < stream_len:
            if stream_len - offset < self.HEADER_STRUCT.size:
                break
                
            frame, player_id, raw_flags = self.HEADER_STRUCT.unpack_from(stream, offset)
            offset += self.HEADER_STRUCT.size
            is_delta = bool(raw_flags & 0x80)
            flags = raw_flags & ~0x80

            if is_delta:
                dx, dy, dz = struct.unpack_from("<hhh", stream, offset)
                offset += 6
                prev = self.history.get(player_id, (0, 0, 0))
                ix, iy, iz = prev[0] + dx, prev[1] + dy, prev[2] + dz
            else:
                ix, iy, iz = struct.unpack_from("<iii", stream, offset)
                offset += 12
                
            self.history[player_id] = (ix, iy, iz)
            yield {
                "frame": frame,
                "player_id": player_id,
                "position": (ix / self.scale, iy / self.scale, iz / self.scale),
                "flags": flags,
                "compressed": is_delta
            }
