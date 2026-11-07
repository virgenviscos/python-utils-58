from typing import Dict, List, Union, Callable

class GameState:
    """Manages state transitions using a function map approach."""
    def __init__(self) -> None:
        self._states: Dict[str, Callable[[], None]] = {}

    def register(self, name: str, callback: Callable[[], None]) -> None:
        """Adds a new state hook to the registry."""
        self._states[name] = callback

    def trigger(self, name: str) -> None:
        """Executes a state callback by key."""
        if name in self._states:
            self._states[name]()

def calculate_dps(base_dmg: float, crit_mult: float, proc_rate: float) -> float:
    """Calculates theoretical damage per second with crit integration."""
    return base_dmg * (1.0 + (crit_mult * proc_rate))

def spawn_entities(count: int, entity_type: str = "goblin") -> List[str]:
    """Generates a list of game entities."""
    return [f"{entity_type}_{i:03d}" for i in range(count)]

if __name__ == "__main__":
    # Example usage for demonstration
    engine = GameState()
    engine.register("idle", lambda: print("System waiting..."))
    engine.trigger("idle")