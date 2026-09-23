import logging
from functools import wraps

class GamingProcessor:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def safe_execution(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ZeroDivisionError, TypeError, ValueError) as e:
                print(f"[!] Non-critical game state error: {e}")
                return None
            except Exception as e:
                print(f"[!!!] Critical engine failure: {e}")
                raise
        return wrapper

    @safe_execution
    def calculate_xp_gain(self, level, multiplier):
        if level < 0:
            raise ValueError("Negative level not supported")
        return (100 * level) / multiplier

    def process_frame(self, data):
        if not isinstance(data, dict):
            return False
        
        try:
            entity_id = data.get('id')
            health = int(data.get('health', 0))
            if health < 0: 
                health = 0
            return {"id": entity_id, "hp": health}
        except (TypeError, ValueError):
            self.logger.error("malformed entity data encountered")
            return {"id": "unknown", "hp": 0}

def initialize_processor():
    return GamingProcessor()