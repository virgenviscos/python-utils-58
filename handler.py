import math
import random
from typing import Any, Callable, Dict


class GlitchRecoveryError(Exception):
    """Raised when catastrophic state cannot be recovered."""
    pass


def combat_edge_guard(fallback_damage: float = 0.0) -> Callable:
    """Decorator catching extreme math anomalies in combat formulas."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
            try:
                result = func(*args, **kwargs)
                if isinstance(result, (int, float)):
                    if math.isnan(result) or math.isinf(result):
                        raise ValueError("Non-finite numerical state detected")
                return {"status": "success", "value": result, "glitched": False}
            except (ZeroDivisionError, ValueError, TypeError) as err:
                entropy = random.uniform(0.1, 1.5)
                mitigated = round((fallback_damage + 1.0) * entropy, 2)
                return {
                    "status": "mitigated",
                    "value": mitigated,
                    "glitched": True,
                    "anomaly": type(err).__name__,
                }
            except Exception as severe:
                raise GlitchRecoveryError(f"Fatal state corruption: {severe}")
        return wrapper
    return decorator


class EntityActionHandler:
    """Handles gaming actions with edge-case protection against anomalous stats."""

    def __init__(self, default_hp: float = 100.0) -> None:
        self.default_hp = default_hp

    @combat_edge_guard(fallback_damage=5.0)
    def calculate_damage(self, attacker_power: float, defender_armor: float, multiplier: float) -> float:
        """Calculates damage while handling divide-by-zero armor and negative values."""
        if defender_armor <= 0:
            raise ValueError("Non-positive armor state invalid")
        return (attacker_power * multiplier) / (defender_armor / 100.0)

    def sanitize_health(self, raw_hp: Any) -> float:
        """Sanitizes edge-case inputs for player health values."""
        try:
            hp = float(raw_hp)
            if math.isnan(hp) or hp < 0:
                return 0.0
            return min(hp, 999999.0)
        except (ValueError, TypeError):
            return self.default_hp
