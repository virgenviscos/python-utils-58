import logging
import time
from logging.handlers import RotatingFileHandler
from typing import Optional


class GameTickFormatter(logging.Formatter):
    """Formatter that injects frame/tick timing into log outputs."""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        super().__init__(
            fmt or "[%(asctime)s][%(levelname)s][TICK:%(tick)d] %(message)s",
            datefmt,
        )
        self._start_time = time.time()

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "tick"):
            # Estimate tick index assuming standard 60 FPS update cycle
            elapsed = time.time() - self._start_time
            record.tick = int(elapsed * 60)
        return super().format(record)


class SessionRotatingHandler(RotatingFileHandler):
    """Rotates log files and writes session boundary markers upon rotation."""

    def doRollover(self) -> None:
        super().doRollover()
        if self.stream:
            self.stream.write("=== LOG ROTATION: NEW SESSION SEGMENT ===\n")
            self.stream.flush()


def setup_game_logger(
    name: str = "game_engine",
    log_file: str = "game_session.log",
    max_bytes: int = 524_288,  # 512 KB
    backup_count: int = 3,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures and returns a tick-aware rotating logger for game engine diagnostics."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    handler = SessionRotatingHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(GameTickFormatter())
    logger.addHandler(handler)

    return logger
