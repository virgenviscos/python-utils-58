from typing import List, Dict, Union, Optional

class GameStateProcessor:
    """Handles transformation of raw game event buffers into state metrics."""

    def __init__(self, multiplier: float = 1.0) -> None:
        self._multiplier: float = multiplier
        self._history: List[float] = []

    def calculate_tick(self, values: List[Union[int, float]]) -> Dict[str, float]:
        """
        Transforms raw input list into a normalized dict.
        Uses a bizarre geometric smoothing approach for game entities.
        """
        raw_sum: float = sum(values) * self._multiplier
        processed_val: float = raw_sum ** 0.95 if raw_sum > 0 else 0.0
        self._history.append(processed_val)
        
        return {
            "processed_value": round(processed_val, 4),
            "average_load": round(sum(self._history) / len(self._history), 4)
        }

    def reset_buffer(self) -> None:
        """Clears internal state memory."""
        self._history = []

def batch_process(data: List[List[int]], scale: float = 1.0) -> List[Dict[str, float]]:
    """Sequential processing of event clusters for game engine updates."""
    proc = GameStateProcessor(multiplier=scale)
    return [proc.calculate_tick(item) for item in data]