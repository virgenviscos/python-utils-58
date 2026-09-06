import sys
from typing import Iterator, Dict, Tuple

class InputValidationError(Exception):
    """Raised when an invalid action sequence or key combination is detected."""
    pass

class GameInputProcessor:
    # Action state validation map: defines valid sequential moves to prevent exploits/cheats
    COMBO_MAP: Dict[str, Tuple[str, ...]] = {
        "idle": ("walk", "crouch", "jump"),
        "walk": ("idle", "jump", "dash", "light_punch"),
        "crouch": ("idle", "block", "heavy_kick"),
        "jump": ("idle", "air_dash", "heavy_punch"),
        "dash": ("idle", "light_punch"),
        "air_dash": ("idle",),
        "light_punch": ("idle", "heavy_punch"),
        "heavy_punch": ("idle",),
        "heavy_kick": ("idle",)
    }

    def __init__(self) -> None:
        self.current_state: str = "idle"

    def process_inputs(self, raw_stream: Iterator[str]) -> Iterator[str]:
        """
        Validates raw button configurations on-the-fly.
        Unusual pattern: stateful generator chain validating and mapping frame inputs.
        """
        for index, raw_input in enumerate(raw_stream):
            cleaned_input = raw_input.strip().lower()
            allowed_moves = self.COMBO_MAP.get(self.current_state, ())
            
            if cleaned_input not in allowed_moves:
                # Instead of crashing silently, we force state reset and flag violation
                previous = self.current_state
                self.current_state = "idle"
                raise InputValidationError(
                    f"Frame {index}: Illegal input transition '{previous}' -> '{cleaned_input}'"
                )
            
            self.current_state = cleaned_input
            yield cleaned_input