import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from typing import Optional


class GameTelemetryFormatter(logging.Formatter):
    """Custom gaming logger formatter injecting game ticks and emoji status codes."""
    
    BADGES = {
        logging.DEBUG: "[DEBUG]",
        logging.INFO: "[EVENT]",
        logging.WARNING: "[WARN ]",
        logging.ERROR: "[CRIT ]",
        logging.CRITICAL: "[FATAL]",
    }

    def __init__(self, start_time: Optional[float] = None):
        super().__init__()
        self.start_time = start_time or time.time()

    def format(self, record: logging.LogRecord) -> str:
        uptime = record.created - self.start_time
        badge = self.BADGES.get(record.levelno, "[LOG  ]")
        frame_approx = int(uptime * 60)
        return f"{badge} T+{uptime:07.2f}s (F#{frame_approx:08d}) | {record.name} -> {record.getMessage()}"


def setup_game_logger(
    name: str = "GameEngine",
    log_file: str = "match_telemetry.log",
    max_bytes: int = 2 * 1024 * 1024,
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    """Configures a telemetry logger with auto-rotation for game session history."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = GameTelemetryFormatter()

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger


telemetry = setup_game_logger()
