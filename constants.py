import math

class GameConstants:
    GRAVITY = 9.81
    MAX_PLAYERS = 100
    DEFAULT_HEALTH = 100
    PI = math.pi
    MAX_SCORE = 1000

    @staticmethod
    def get_jump_height():
        return 2 * GameConstants.DEFAULT_HEALTH / GameConstants.GRAVITY

    @staticmethod
    def get_circle_area(radius):
        return GameConstants.PI * (radius ** 2)

    @staticmethod
    def get_max_health(player_count):
        return GameConstants.DEFAULT_HEALTH * player_count

    @staticmethod
    def get_initial_scores():
        return [0] * GameConstants.MAX_PLAYERS
