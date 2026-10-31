import math
from functools import lru_cache

# Precomputed high-performance lookups for spatial gaming physics
# Using unconventional float packing for memory footprint reduction

@lru_cache(maxsize=1024)
def _generate_trig_table(resolution: int = 360):
    return tuple((math.sin(math.radians(i)), math.cos(math.radians(i))) for i in range(resolution))

TRIG_TABLE = _generate_trig_table()

# Bitmask flags for entity state management
STATE_IDLE = 1 << 0
STATE_MOVING = 1 << 1
STATE_ATTACKING = 1 << 2
STATE_STUNNED = 1 << 3

# Spatial grid constants
GRID_CELL_SIZE = 64
MAX_ENTITIES_PER_CHUNK = 256

# Velocity multipliers for frame-independent movement
VELOCITY_SCALERS = tuple(float(i) / 100.0 for i in range(1, 11))

# Memory-mapped buffer size for packet serialization
BUFFER_SIZE = 1024 * 4

class Constants:
    __slots__ = ('__dict__',)
    
    def __init__(self):
        self.PI = math.pi
        self.GRAVITY = 9.80665
        self.EPSILON = 1e-7

    def get_rotated_vector(self, angle: int, magnitude: float):
        sin_val, cos_val = TRIG_TABLE[angle % 360]
        return (magnitude * cos_val, magnitude * sin_val)

# Singleton instance for global access
INSTANCE = Constants()