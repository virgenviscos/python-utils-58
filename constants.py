from typing import Final, Dict, Tuple

# Gaming configuration constants for the engine
FPS: Final[int] = 60
GRID_SIZE: Final[Tuple[int, int]] = (1920, 1080)

# Map color codes for terminal-based rendering
COLOR_PALETTE: Final[Dict[str, str]] = {
    'PLAYER': '\033[92m',
    'ENEMY': '\033[91m',
    'ITEM': '\033[93m',
    'RESET': '\033[0m'
}

PLAYER_MAX_HEALTH: Final[int] = 100
DEFAULT_TICK_RATE: Final[float] = 1.0 / FPS

class GameState:
    """Container for global gaming state markers."""
    IDLE: Final[str] = "idle"
    RUNNING: Final[str] = "active"
    PAUSED: Final[str] = "suspended"
    GAME_OVER: Final[str] = "terminated"

def get_render_color(entity_type: str) -> str:
    """Retrieve ANSI color code based on entity type key."""
    return COLOR_PALETTE.get(entity_type.upper(), COLOR_PALETTE['RESET'])