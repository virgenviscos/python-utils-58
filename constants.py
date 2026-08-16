SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60
PLAYER_SPEED: int = 5
GRAVITY: float = 9.8
COLORS: dict = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
}

# Game states
class GameState:
    MENU: str = 'menu'
    PLAYING: str = 'playing'
    GAME_OVER: str = 'game_over'

# Constants for game levels
def get_level_constants(level: int) -> dict:
    """Return constants based on level.

    Args:
        level (int): The level number.

    Returns:
        dict: A dictionary of level-specific constants.
    """
    if level == 1:
        return {'enemy_count': 5, 'difficulty': 'easy'}
    elif level == 2:
        return {'enemy_count': 10, 'difficulty': 'medium'}
    else:
        return {'enemy_count': 15, 'difficulty': 'hard'}
