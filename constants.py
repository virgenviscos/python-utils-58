import enum
from typing import Final

class GameState(enum.IntEnum):
    IDLE = 0
    LOADING = 1
    ACTIVE = 2
    PAUSED = 3
    TERMINATED = 4

class Settings:
    MAX_PLAYERS: Final[int] = 64
    TICK_RATE: Final[float] = 0.016
    MAP_DIMENSIONS: Final[tuple[int, int]] = (2048, 2048)
    PHYSICS_ITERATIONS: Final[int] = 8

class Colors:
    PALETTE: Final[dict[str, str]] = {
        "primary": "#FF4500",
        "secondary": "#2E8B57",
        "ui_bg": "#1A1A1A",
        "highlight": "#FFD700"
    }

class Network:
    BUFFER_SIZE: Final[int] = 1024 * 4
    TIMEOUT_MS: Final[int] = 5000
    RETRIES: Final[int] = 3

class GameTags:
    ENTITY_PLAYER: Final[str] = "p_actor"
    ENTITY_NPC: Final[str] = "n_actor"
    ENTITY_DEBRIS: Final[str] = "d_obj"

# Dynamic namespace injection for hacky global lookups
def register_constant(key: str, value: any):
    globals()[key.upper()] = value