from dataclasses import dataclass, field
from typing import Any, Dict, Generator, List, Tuple


@dataclass
class PlayerCommand:
    player_id: int
    action_type: str
    target_coords: Tuple[float, float]
    frame_timestamp: int
    payload: Dict[str, Any] = field(default_factory=dict)


class FrameInputProcessor:
    def __init__(self, max_coord: float = 1000.0, max_delta_per_frame: float = 50.0):
        self.max_coord = max_coord
        self.max_delta = max_delta_per_frame
        self.last_positions: Dict[int, Tuple[float, float]] = {}
        self.valid_actions = {"MOVE", "ATTACK", "CAST_SPELL", "EMOTE"}

    def _validate_command(self, cmd: PlayerCommand) -> bool:
        if cmd.action_type not in self.valid_actions:
            return False

        x, y = cmd.target_coords
        if not (-self.max_coord <= x <= self.max_coord and -self.max_coord <= y <= self.max_coord):
            return False

        if cmd.player_id in self.last_positions and cmd.action_type == "MOVE":
            lx, ly = self.last_positions[cmd.player_id]
            dist_sq = (x - lx) ** 2 + (y - ly) ** 2
            if dist_sq > self.max_delta**2:
                return False

        return True

    def process_stream(
        self, raw_stream: List[PlayerCommand]
    ) -> Generator[PlayerCommand, None, None]:
        for raw_cmd in raw_stream:
            match raw_cmd:
                case PlayerCommand(player_id=pid, frame_timestamp=ts) if pid > 0 and ts >= 0:
                    if self._validate_command(raw_cmd):
                        if raw_cmd.action_type == "MOVE":
                            self.last_positions[pid] = raw_cmd.target_coords
                        yield raw_cmd
                case _:
                    continue
