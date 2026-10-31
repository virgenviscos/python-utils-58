import math
from typing import Dict, Any, Generator, Callable, List

class InvalidGameInputError(Exception):
    """Raised when a player input packet violates bounds or schema."""
    pass

def validate_spatial_bounds(data: Dict[str, Any]) -> bool:
    x, y, z = data.get("pos", (0.0, 0.0, 0.0))
    return all(-10000 <= axis <= 10000 for axis in (x, y, z)) and not any(math.isnan(axis) for axis in (x, y, z))

def validate_action_cooldown(data: Dict[str, Any]) -> bool:
    action = data.get("action")
    timestamp = data.get("ts", 0)
    return isinstance(action, (str, type(None))) and isinstance(timestamp, (int, float)) and timestamp >= 0

class FrameInputProcessor:
    def __init__(self):
        self._rules: List[Callable[[Dict[str, Any]], bool]] = [
            validate_spatial_bounds,
            validate_action_cooldown
        ]

    def sanitize_stream(self, raw_frames: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop with pipeline-style input validation."""
        for frame_id, frame in enumerate(raw_frames):
            if not isinstance(frame, dict):
                continue

            validation_matrix = (rule(frame) for rule in self._rules)
            if not all(validation_matrix):
                frame["corrupted"] = True
                frame["pos"] = (0.0, 0.0, 0.0)
                frame["action"] = "idle"
            else:
                frame["corrupted"] = False

            if "pos" in frame and not frame["corrupted"]:
                frame["pos"] = tuple(round(float(v), 3) for v in frame["pos"])

            yield {"frame_id": frame_id, **frame}

def process_game_inputs(raw_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    processor = FrameInputProcessor()
    return [frame for frame in processor.sanitize_stream(raw_stream) if not frame.get("corrupted")]
