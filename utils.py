import math
from functools import wraps
from typing import Callable, Any, Dict

class CombatMathError(ArithmeticError):
    """Raised when combat calculations hit nonsensical mathematical bounds."""
    pass

def safeguard_combat_math(fallback_value: float = 0.0) -> Callable:
    """Decorator catching game-breaking edge cases in combat calculations."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> float:
            try:
                result = func(*args, **kwargs)
                if not isinstance(result, (int, float)):
                    raise TypeError(f"Expected numeric result, got {type(result).__name__}")
                if math.isnan(result):
                    raise CombatMathError("Calculation resulted in NaN")
                if math.isinf(result):
                    return math.copysign(999999.0, result)
                return float(result)
            except (ZeroDivisionError, OverflowError, TypeError, CombatMathError) as exc:
                if isinstance(exc, ZeroDivisionError):
                    return 999999.0 if fallback_value > 0 else 0.0
                return fallback_value
        return wrapper
    return decorator

@safeguard_combat_math(fallback_value=1.0)
def calculate_effective_damage(raw_damage: float, armor: float, armor_pen: float = 0.0) -> float:
    """Calculates net damage dealt considering armor mitigation and edge cases."""
    effective_armor = max(0.0, armor - armor_pen)
    if effective_armor == 0:
        return float(raw_damage)
    mitigation = 100.0 / effective_armor
    damage = raw_damage * (1.0 - (mitigation / 100.0))
    if damage < 0:
        raise CombatMathError("Heal-on-hit overflow detected from negative damage")
    return damage

def sanitize_player_stats(stats: Dict[str, Any]) -> Dict[str, float]:
    """Edge case sanitizer for corrupted or tampered player state dictionaries."""
    defaults = {"hp": 100.0, "mana": 50.0, "speed": 1.0, "attack": 10.0}
    cleaned = {}
    for key, default_val in defaults.items():
        val = stats.get(key, default_val)
        try:
            num_val = float(val)
            cleaned[key] = max(0.0, num_val) if not math.isnan(num_val) else default_val
        except (ValueError, TypeError):
            cleaned[key] = default_val
    return cleaned