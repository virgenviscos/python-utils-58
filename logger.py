import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, Any

class ArcadeLogFormatter(logging.Formatter):
    """Custom formatter that injects game-themed visual indicators into logs."""
    ICON_MAP = {
        "DEBUG": "[🔍 DBG]",
        "INFO": "[⚔️ ACT]",
        "WARNING": "[⚠️ WRN]",
        "ERROR": "[💥 ERR]",
        "CRITICAL": "[☠️ KO!]"
    }

    def format(self, record: logging.LogRecord) -> str:
        icon = self.ICON_MAP.get(record.levelname, f"[{record.levelname}]")
        record.game_icon = icon
        return super().format(record)


class MatchSessionRotatingHandler(RotatingFileHandler):
    """Rotating file handler capable of forcing rollover when a game match changes."""
    def __init__(self, filename: str, max_bytes: int = 512 * 1024, backup_count: int = 5):
        super().__init__(filename, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")

    def rotate_for_new_match(self, match_id: str) -> None:
        """Manually force log rotation upon starting a new game match."""
        if self.stream:
            self.stream.flush()
            self.stream.close()
            self.stream = None
        self.doRollover()
        if self.stream:
            self.stream.write(f"=== MATCH START: {match_id} ===\n")
            self.stream.flush()


def setup_game_logger(
    logger_name: str = "game_telemetry",
    file_path: str = "session.log",
    max_kb: int = 256,
    backups: int = 3
) -> logging.Logger:
    """Configures and returns a rotating logger setup tailored for gaming metrics."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = MatchSessionRotatingHandler(file_path, max_bytes=max_kb * 1024, backup_count=backups)
        fmt = "%(asctime)s | %(game_icon)s | %(name)s :: %(message)s"
        formatter = ArcadeLogFormatter(fmt=fmt, datefmt="%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
