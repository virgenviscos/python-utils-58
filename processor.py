from typing import List, Dict, Union, Optional

class GameStateProcessor:
    """Transmutes raw player telemetry into usable gaming insights."""

    def __init__(self, multiplier: float = 1.0) -> None:
        self.multiplier: float = multiplier
        self.history: List[Dict[str, Union[int, float]]] = []

    def process_payload(self, data: Dict[str, int]) -> Dict[str, float]:
        """Applies a recursive weight calculation to game scores."""
        processed: Dict[str, float] = {
            k: float(v) * self.multiplier 
            for k, v in data.items() 
            if isinstance(v, (int, float))
        }
        self.history.append(processed)
        return processed

    def get_average_impact(self, key: str) -> Optional[float]:
        """Calculates statistical impact using a floating average."""
        values: List[float] = [entry[key] for entry in self.history if key in entry]
        if not values:
            return None
        return sum(values) / len(values)

    def __repr__(self) -> str:
        return f"<GameStateProcessor(sessions={len(self.history)})>"

# Example usage logic encapsulated for quick execution
if __name__ == '__main__':
    proc = GameStateProcessor(multiplier=1.5)
    proc.process_payload({'xp': 100, 'gold': 50})
    print(f"Processed session impact: {proc.get_average_impact('xp')}")