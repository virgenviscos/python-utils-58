import time
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


class TelemetryFilter(logging.Filter):
    """Attaches game session uptime info to log records."""

    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id
        self.start_time = time.time()

    def filter(self, record: logging.LogRecord) -> bool:
        record.uptime = f"{time.time() - self.start_time:.2f}s"
        record.session_id = self.session_id
        return True


class GameSessionLogRotator(RotatingFileHandler):
    """Rotating log handler that stamps a session header upon rollover."""

    def doRollover(self):
        super().doRollover()
        if self.stream:
            self.stream.write("=== SESSION ROTATION MARKER ===\n")
            self.stream.flush()


def setup_game_logger(
    logger_name: str = "game_telemetry",
    log_file: str = "game_events.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    session_id: Optional[str] = None,
) -> logging.Logger:
    """Configures a rotating logger with telemetry metadata for game events."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    sess_id = session_id or f"sess_{int(time.time())}"
    logger.addFilter(TelemetryFilter(session_id=sess_id))

    formatter = logging.Formatter(
        fmt="[%(asctime)s][%(session_id)s][T+%(uptime)s][%(levelname)s] >> %(message)s",
        datefmt="%H:%M:%S",
    )

    file_handler = GameSessionLogRotator(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info(f"Telemetry logger initialized for session {sess_id}")
    return logger
