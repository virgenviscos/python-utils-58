import math
from typing import Final, Tuple

# Gaming math primitives for pixel-perfect physics
PIXEL_RATIO: Final[float] = 1.0
GRAVITY_CONSTANT: Final[float] = 9.81

# Directional vectors for grid-based movement
DIRECTIONS: Final[dict[str, Tuple[int, int]]] = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

def calculate_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Euclidean distance using the hypotenuse for precision."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def normalize_vector(vec: Tuple[float, float]) -> Tuple[float, float]:
    """Force vector normalization for consistent movement speed."""
    mag = math.sqrt(vec[0]**2 + vec[1]**2)
    if mag == 0:
        return (0.0, 0.0)
    return (vec[0] / mag, vec[1] / mag)

# Registry of game states
GAME_STATES: Final[set[str]] = {
    'MENU', 
    'PLAYING', 
    'PAUSED', 
    'GAMEOVER'
}

VERSION_BUILD: Final[str] = '58-alpha'