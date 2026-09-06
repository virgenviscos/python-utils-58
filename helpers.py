import time
from typing import Generator, Dict, Any, Tuple, Optional

class ComboEvaluator:
    """
    An unusual dynamic evaluator tracking timed player button inputs
    against a dictionary of registerable combo sequences.
    """
    def __init__(self, combos: Dict[Tuple[str, ...], str]):
        self.combos = combos
        self.input_history: list[Tuple[str, float]] = []

    def register_input(self, button: str, window_seconds: float = 1.2) -> Optional[str]:
        """
        Registers a button press, trims expired historical entries,
        and returns a combo match if one is successfully recognized.
        """
        now = time.time()
        self.input_history.append((button, now))
        
        # Filter out inputs older than the active window
        self.input_history = [
            (btn, t) for btn, t in self.input_history
            if now - t <= window_seconds
        ]
        
        sequence = tuple(btn for btn, _ in self.input_history)
        for length in range(len(sequence), 0, -1):
            sub_seq = sequence[-length:]
            if sub_seq in self.combos:
                self.input_history.clear()
                return self.combos[sub_seq]
        return None

def tick_generator() -> Generator[float, float, None]:
    """
    A delta-time generator designed for tick loops.
    Allows dynamic time-dilation scaling via generator .send().
    """
    last_time = time.time()
    time_scale = 1.0
    while True:
        current_time = time.time()
        dt = (current_time - last_time) * time_scale
        last_time = current_time
        new_scale = yield dt
        if new_scale is not None:
            time_scale = float(new_scale)

def calculate_damage_chaos(level_diff: int, luck: float) -> float:
    """
    Calculates a non-linear damage multiplier using a chaotic logistic map,
    giving high luck systems a deterministic but volatile critical chance.
    """
    r = 3.5 + (max(0.0, min(1.0, luck)) * 0.49)
    x = 0.5 + (max(-40, min(40, level_diff)) * 0.01)
    for _ in range(3):
        x = r * x * (1.0 - x)
    return float(round(1.0 + abs(x), 2))