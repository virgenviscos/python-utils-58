import math
from typing import Any, Dict, Tuple, Union, Callable
from functools import wraps

class GamingValidationError(ValueError):
    """Raised when game state metrics breach unrecoverable thresholds."""
    pass

def sanitize_spatial_coords(fallback_origin: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
    """Decorator to sanitize spatial vector edge cases (NaN, Inf, absurd bounds)."""
    def decorator(func: Callable[..., Tuple[float, float, float]]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[float, float, float]:
            try:
                coords = func(*args, **kwargs)
                if not isinstance(coords, (tuple, list)) or len(coords) != 3:
                    return fallback_origin
                
                sanitized = []
                for val in coords:
                    if not isinstance(val, (int, float)) or math.isnan(val) or math.isinf(val):
                        sanitized.append(0.0)
                    else:
                        # Clamp coordinate boundary to prevent map-escape bugs
                        sanitized.append(max(-100000.0, min(100000.0, float(val))))
                return (sanitized[0], sanitized[1], sanitized[2])
            except Exception as err:
                raise GamingValidationError(f"Spatial parsing failed for payload: {err}") from err
        return wrapper
    return decorator

class PlayerMetricValidator:
    """Validation pipeline for player stats with resilient edge case recovery."""

    @staticmethod
    def validate_health(raw_hp: Any, max_hp: float = 100.0) -> float:
        """Handles string inputs, negative overflow, and extreme non-numeric junk."""
        try:
            hp = float(raw_hp)
            if math.isnan(hp):
                return 0.0
            if math.isinf(hp):
                return max_hp if hp > 0 else 0.0
            return max(0.0, min(max_hp, hp))
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    @sanitize_spatial_coords(fallback_origin=(0.0, 64.0, 0.0))
    def validate_spawn_point(pos: Dict[str, Any]) -> Tuple[float, float, float]:
        """Extracts X, Y, Z handling missing keys, string numbers, and bad telemetry."""
        if not isinstance(pos, dict):
            return (0.0, 64.0, 0.0)
        x = pos.get('x', 0.0)
        y = pos.get('y', 64.0)
        z = pos.get('z', 0.0)
        return (float(x), float(y), float(z))
