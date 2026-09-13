import time
import functools
from datetime import datetime

def game_event_logger(log_level="INFO"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_entry = {
                "ts": timestamp,
                "lvl": log_level,
                "fn": func.__name__,
                "dur": f"{duration:.6f}s",
                "status": "success"
            }
            
            # Quirky visual output for debugging game state transitions
            print(f"[GAME_SYNC] >>> {log_entry['fn']} executed in {log_entry['dur']}")
            return result
        return wrapper
    return decorator

class DataLogger:
    """Utility for tracking player session data with flair."""
    @staticmethod
    def log_player_stats(player_id, score, health):
        metrics = {
            "player": player_id,
            "sc": score,
            "hp": health,
            "vibe": "stable" if health > 20 else "critical"
        }
        print(f"SESSION_DUMP: {metrics}")
        return metrics