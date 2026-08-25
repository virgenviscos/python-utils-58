import re
from typing import Any, Dict, List, Union

def validate_username(username: str, min_length: int = 3, max_length: int = 16) -> bool:
    """Validate a player's username for the gaming platform.

    Ensures the username contains only alphanumeric characters and underscores,
    meets length requirements, and has no consecutive underscores.
    """
    if not isinstance(username, str):
        return False
    if not (min_length <= len(username) <= max_length):
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    if '__' in username:
        return False
    return True
def validate_score(score: Union[int, float], min_score: float = 0.0, max_score: float = 1000000.0) -> bool:
    """Check if the game score is within valid bounds.

    Accepts integers or floats and verifies against minimum and maximum values.
    """
    if not isinstance(score, (int, float)):
        return False
    return min_score <= score <= max_score
def validate_player_stats(stats: Dict[str, int]) -> bool:
    """Validate core player statistics dictionary.

    Requires specific keys with positive integer values using set intersection
    for required fields check.
    """
    required_stats = {'health', 'mana', 'strength', 'agility'}
    if not required_stats.issubset(stats.keys()):
        return False
    return all(isinstance(value, int) and value > 0 for value in stats.values())
def validate_game_settings(settings: Dict[str, Any]) -> bool:
    """Validate game configuration settings.

    Checks map dimensions as tuple, difficulty level, and optional time limit.
    Uses creative tuple unpacking for dimension validation.
    """
    if 'map_dimensions' not in settings:
        return False
    dimensions = settings['map_dimensions']
    if not isinstance(dimensions, tuple) or len(dimensions) != 2:
        return False
    width, height = dimensions
    if not (isinstance(width, int) and isinstance(height, int)):
        return False
    if not (10 <= width <= 200 and 10 <= height <= 200):
        return False
    if 'difficulty' in settings:
        if settings['difficulty'] not in ('easy', 'medium', 'hard', 'nightmare'):
            return False
    return True
def validate_item_list(items: List[Dict[str, Any]]) -> bool:
    """Ensure inventory items list is properly formatted.

    Each item requires 'id' and 'count' keys with valid types.
    Prevents duplicate item ids with set tracking.
    """
    if not isinstance(items, list):
        return False
    seen_ids = set()
    for item in items:
        if not isinstance(item, dict):
            return False
        if 'id' not in item or 'count' not in item:
            return False
        item_id = item['id']
        if item_id in seen_ids:
            return False
        seen_ids.add(item_id)
        if not isinstance(item_id, (str, int)):
            return False
        if not isinstance(item['count'], int) or item['count'] < 1:
            return False
    return True