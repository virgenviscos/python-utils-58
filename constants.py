from typing import Generic, TypeVar, Final, Dict, Any

N = TypeVar('N', int, float)

class ScalableStatic(Generic[N]):
    """A game constant that remains immutable but can spawn scaled variants.

    Perfect for balancing damage scaling or physics constants across game difficulties.
    """
    def __init__(self, base_value: N) -> None:
        object.__setattr__(self, "_base", base_value)

    @property
    def base(self) -> N:
        """The pristine, unmutated root value of this game metric."""
        return self._base

    def scale(self, factor: float) -> float:
        """Calculate a temporary variant scaled by game-loop dynamics."""
        return float(self._base * factor)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Denied: Static game elements must not be mutated.")

    def __repr__(self) -> str:
        return f"ScalableStatic(base={self._base})"

# Core engine & environment mechanics
GRAVITY: Final[ScalableStatic[float]] = ScalableStatic(-9.81)
TICK_RATE_HZ: Final[int] = 60

# Player core attributes
BASE_STAMINA: Final[ScalableStatic[int]] = ScalableStatic(100)
DASH_COOLDOWN_SEC: Final[ScalableStatic[float]] = ScalableStatic(1.5)

# Global lookup registry for debugging sandbox modes
GAME_REGISTRY: Final[Dict[str, ScalableStatic[Any]]] = {
    "gravity": GRAVITY,
    "stamina": BASE_STAMINA,
    "dash_cooldown": DASH_COOLDOWN_SEC
}
