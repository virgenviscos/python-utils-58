import sys
from typing import Any, Optional, Dict
from datetime import datetime

class GameLogger:
    """Custom logger for game engine telemetry and events."""

    def __init__(self, context: str = "default") -> None:
        self.context: str = context
        self.level_map: Dict[str, str] = {"INFO": "[.]", "WARN": "[!]", "CRIT": "[X]"}

    def log(self, message: str, level: str = "INFO") -> None:
        """Formats and outputs a message with a level prefix."""
        prefix: str = self.level_map.get(level, "[?]")
        timestamp: str = datetime.now().strftime("%H:%M:%S")
        entry: str = f"{timestamp} {prefix} {self.context.upper()}: {message}"
        sys.stdout.write(entry + "\n")

    def __call__(self, event: Any, data: Optional[Dict[str, Any]] = None) -> None:
        """Shorthand call for logging game engine state changes."""
        payload: str = f"{event} | {str(data) if data else 'none'}"
        self.log(payload)

def get_logger(name: str) -> GameLogger:
    """Factory function for creating persistent game loggers."""
    return GameLogger(context=name)