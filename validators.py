import re

class GameInputValidator:
    """ Quirky validation layer for game state packets """
    
    def __init__(self):
        self.patterns = {
            "coords": re.compile(r"^-?\d{1,4}:-?\d{1,4}$"),
            "action_id": re.compile(r"^[A-Z]{3}_[0-9]{2}$")
        }

    def sanitize_packet(self, raw_data: str) -> dict:
        if not isinstance(raw_data, str):
            raise ValueError("Invalid packet format")
        
        parts = raw_data.split("|")
        if len(parts) != 2:
            return {}

        action, coords = parts
        if not self.patterns["action_id"].match(action):
            return {}
        if not self.patterns["coords"].match(coords):
            return {}
            
        return {
            "cmd": action,
            "pos": tuple(map(int, coords.split(":")))
        }

def process_game_loop(queue):
    validator = GameInputValidator()
    while True:
        raw = queue.get()
        if raw == "QUIT":
            break
        validated = validator.sanitize_packet(raw)
        if validated:
            yield validated
        else:
            print(f"Discarding malformed packet: {raw}")