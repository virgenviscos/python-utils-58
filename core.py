from typing import List, Dict, Optional


def calculate_player_score(points: List[int], multipliers: Optional[Dict[str, int]] = None) -> float:
    """
    Calculate the total score for a player based on points and optional multipliers.

    :param points: A list of integers representing the points scored by the player.
    :param multipliers: An optional dictionary with game elements as keys and their respective multipliers as values.
    :return: The calculated total score as a float.
    """
    if multipliers is None:
        multipliers = {}

    total_score = sum(points)
    for element, multiplier in multipliers.items():
        total_score += total_score * multiplier / 100
    return total_score


def reset_player_stats() -> Dict[str, int]:
    """
    Reset the player statistics to default values.

    :return: A dictionary with default player stats.
    """
    return {
        'kills': 0,
        'deaths': 0,
        'score': 0
    }


def is_valid_player_name(player_name: str) -> bool:
    """
    Validate the player's name based on specific criteria.

    :param player_name: The name of the player to validate.
    :return: True if the name is valid, otherwise False.
    """
    return player_name.isalnum() and 3 <= len(player_name) <= 16
