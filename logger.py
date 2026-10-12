import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


class GameSessionFormatter(logging.Formatter):
    """Custom log formatter prefixing HUD metadata and combat flags."""

    def __init__(self, session_id: str = "GAME-SESSION-001"):
        super().__init__(
            fmt="[%(asctime)s][%(levelname)s][%(session)s] %(message)s",
            datefmt="%H:%M:%S",
        )
        self.session_id = session_id

    def format(self, record: logging.LogRecord) -> str:
        record.session = getattr(record, "session", self.session_id)
        if record.levelno >= logging.ERROR:
            record.msg = f"[FATAL_DAMAGE] {record.msg}"
        return super().format(record)


def setup_game_logger(
    name: str = "game_engine",
    log_file: str = "logs/game_events.log",
    max_bytes: int = 512 * 1024,
    backup_count: int = 3,
    session_id: Optional[str] = None,
) -> logging.Logger:
    """Builds a rotating log infrastructure for streaming game events."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        logger.handlers.clear()

    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        GameSessionFormatter(session_id=session_id or "MATCH-LOBBY")
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(levelname)s >> %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
