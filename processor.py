import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class InputProcessor:
    def __init__(self, schema: Dict[str, type]):
        self.schema = schema

    def validate_input(self, data: Dict[str, Any]) -> bool:
        try:
            for key, expected_type in self.schema.items():
                if key not in data or not isinstance(data[key], expected_type):
                    raise ValueError(f"missing or invalid type for {key}")
            return True
        except ValueError as e:
            logger.warning(f"malformed packet dropped: {e}")
            return False

    def process_loop(self, queue: list):
        """Main gaming loop processing frame inputs."""
        while queue:
            packet = queue.pop(0)
            if self.validate_input(packet):
                self.execute_game_logic(packet)

    def execute_game_logic(self, packet: Dict[str, Any]):
        # Game state mutation magic
        pass

if __name__ == "__main__":
    # Example usage for a movement packet
    proc = InputProcessor({"x": int, "y": int, "id": str})
    proc.process_loop([{"x": 10, "y": 20, "id": "player_1"}])