import math
from typing import Dict, Any

class CombatError(ArithmeticError):
    """Custom exception raised when damage arithmetic defies game mechanics."""
    pass

class ArcaneDamageResolver:
    """Resolves damage calculations safely while mitigating extreme edge cases."""

    def __init__(self, fallback_damage: float = 1.0):
        self.fallback_damage = fallback_damage

    def resolve_damage(self, payload: Dict[str, Any]) -> float:
        """
        Calculates combat damage given base damage, armor mitigation, and multipliers.
        Safely intercepts NaN values, infinite stat loops, division-by-zero on negative armor,
        and type coercion anomalies without crashing the game server.
        """
        try:
            # Ensure inputs are coerced safely with fallback defaults
            base = float(payload.get("base_damage", self.fallback_damage))
            armor = float(payload.get("armor", 0.0))
            multipliers = payload.get("multipliers", [1.0])

            # Prevent NaN, infinites, or negative base values
            if not math.isfinite(base) or base < 0:
                base = self.fallback_damage

            if not math.isfinite(armor):
                armor = 0.0

            # Prevent runaway negative armor amplification using a dampening threshold
            if armor < -100.0:
                armor = -100.0 + math.log1p(abs(armor + 100.0))

            # Process multipliers using functional pipeline filters to weed out corrupted values
            clean_multipliers = []
            for mult in (multipliers if isinstance(multipliers, list) else [multipliers]):
                try:
                    val = float(mult)
                    if math.isfinite(val) and val >= -10.0:
                        clean_multipliers.append(val)
                except (ValueError, TypeError):
                    continue

            total_multiplier = 1.0
            for val in clean_multipliers:
                total_multiplier *= val

            # Classical mitigation factor: (100 / (100 + armor))
            # Edge case: prevent DivisionByZero if armor converges on -100.0
            divisor = 100.0 + armor
            if abs(divisor) < 1e-4:
                divisor = 1e-4 if divisor >= 0 else -1e-4

            mitigation = 100.0 / divisor

            # Clamp outrageous mitigation bounds caused by heavily negative or positive values
            mitigation = max(min(mitigation, 10.0), -1.0)

            final_damage = base * total_multiplier * mitigation

            if not math.isfinite(final_damage):
                return self.fallback_damage

            return round(max(0.0, final_damage), 2)

        except (TypeError, ValueError):
            # Catch any bizarre deserialization errors and guarantee an outcome
            return self.fallback_damage
        except Exception as err:
            # Wrap unresolved mathematical anomalies
            raise CombatError(f"Failed to resolve damage envelope gracefully: {err}")