import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class GamingLogFormatter(logging.Formatter):
    """Custom gaming-themed log formatter with level indicators."""
    LEVEL_BADGES = {
        logging.DEBUG: "🎮 [DEBUG]",
        logging.INFO: "⚔️  [INFO ]",
        logging.WARNING: "⚠️  [WARN ]",
        logging.ERROR: "💥 [CRIT ]",
        logging.CRITICAL: "💀 [FATAL]",
    }

    def format(self, record):
        badge = self.LEVEL_BADGES.get(record.levelno, "[LOG]")
        frame_tick = getattr(record, "tick", 0)
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S.%f")[:-3]
        record.formatted_prefix = f"{timestamp} | Frame:{frame_tick:06d} | {badge}"
        return super().format(record)

def setup_game_logger(
    logger_name: str = "game_engine",
    log_file: str = "game_session.log",
    max_megabytes: int = 5,
    backup_count: int = 3,
    debug_mode: bool = False
) -> logging.Logger:
    """Configures a rotating log handler with gaming telemetry tags."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    logger.handlers.clear()

    max_bytes = max_megabytes * 1024 * 1024
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )

    fmt = "%(formatted_prefix)s :: %(message)s"
    formatter = GamingLogFormatter(fmt)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

class LogFrameAdapter(logging.LoggerAdapter):
    """Adapter injecting game tick / frame numbers into log records."""
    def __init__(self, logger: logging.Logger, current_tick: int = 0):
        super().__init__(logger, {"tick": current_tick})
        self.tick = current_tick

    def process(self, msg, kwargs):
        kwargs["extra"] = kwargs.get("extra", {})
        kwargs["extra"]["tick"] = self.tick
        return msg, kwargs