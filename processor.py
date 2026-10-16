from typing import List, Dict, Union, Optional

class GameStateProcessor:
    """Processes raw gaming event telemetry into structured format."""

    def __init__(self, multiplier: float = 1.0) -> None:
        self._multiplier: float = multiplier

    def process_scores(self, raw_data: List[Union[int, float]]) -> List[float]:
        """Applies global multiplier to a batch of player scores."""
        return [float(score * self._multiplier) for score in raw_data]

    def aggregate_stats(self, data_map: Dict[str, List[int]]) -> Dict[str, float]:
        """Calculates average values per stat category mapping."""
        results: Dict[str, float] = {}
        for key, values in data_map.items():
            if not values:
                results[key] = 0.0
                continue
            results[key] = sum(values) / len(values)
        return results

    def get_rank_bracket(self, score: float) -> str:
        """Categorizes player performance based on raw score thresholds."""
        brackets: List[tuple[int, str]] = [
            (1000, "Elite"),
            (500, "Pro"),
            (0, "Novice")
        ]
        for limit, label in brackets:
            if score >= limit:
                return label
        return "Unranked"

    def toggle_boost(self, active: bool) -> None:
        """Dynamic modifier adjustment for gameplay telemetry scaling."""
        self._multiplier = 2.0 if active else 1.0