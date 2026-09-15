import math
from functools import lru_cache

# Precomputed lookup tables for low-latency game math
# Utilizing memoization for expensive trigonometric cycles in game world rotation

TABLE_SIZE = 1024

@lru_cache(maxsize=1)
def _generate_sin_table():
    return [math.sin(2 * math.pi * i / TABLE_SIZE) for i in range(TABLE_SIZE)]

@lru_cache(maxsize=1)
def _generate_cos_table():
    return [math.cos(2 * math.pi * i / TABLE_SIZE) for i in range(TABLE_SIZE)]

SIN_LOOKUP = _generate_sin_table()
COS_LOOKUP = _generate_cos_table()

class PhysicsConstants:
    GRAVITY = 9.81
    DRAG_COEFFICIENT = 0.47
    TICK_RATE = 60
    DELTA_TIME = 1.0 / TICK_RATE

    @staticmethod
    def get_fast_sin(index: int) -> float:
        return SIN_LOOKUP[index % TABLE_SIZE]

    @staticmethod
    def get_fast_cos(index: int) -> float:
        return COS_LOOKUP[index % TABLE_SIZE]

# Bitwise masks for entity status flagging in memory-constrained environments
ENTITY_ALIVE = 1 << 0
ENTITY_VISIBLE = 1 << 1
ENTITY_INTERACTABLE = 1 << 2
ENTITY_NETWORK_SYNC = 1 << 3