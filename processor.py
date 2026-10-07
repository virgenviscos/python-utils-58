import struct
from typing import Generator, Tuple

class GamePacketProcessor:
    """Processes and validates raw incoming byte streams for multiplayer game events."""

    HEADER = 0x7E

    def __init__(self) -> None:
        self._buffer = bytearray()

    def process_stream(self, chunk: bytes) -> Generator[Tuple[bool, bytes], None, None]:
        """Validates stream inputs on the fly, emitting verified payloads."""
        self._buffer.extend(chunk)
        
        while len(self._buffer) >= 4:
            if self._buffer[0] != self.HEADER:
                self._buffer.pop(0)
                continue

            packet_len = self._buffer[1]
            if packet_len < 4 or packet_len > 128:
                self._buffer.pop(0)
                continue

            if len(self._buffer) < packet_len:
                break

            packet = self._buffer[:packet_len]
            del self._buffer[:packet_len]

            if self._validate_packet(packet):
                # Yields True and the isolated event payload
                yield True, bytes(packet[2:-1])
            else:
                # Yields False and the corrupted raw packet
                yield False, bytes(packet)

    def _validate_packet(self, packet: bytearray) -> bool:
        """Performs XOR checksum validation and validates event bounds."""
        if len(packet) < 4:
            return False
            
        checksum = 0
        for byte in packet[:-1]:
            checksum ^= byte
            
        if checksum != packet[-1]:
            return False

        # Dynamic game validation constraint for incoming commands
        opcode = packet[2]
        return opcode in {0x01, 0x02, 0x03, 0x04}
