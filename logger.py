import logging
from logging.handlers import RotatingFileHandler
import os

LOG_LEVEL = logging.INFO
LOG_FILE = "game_engine.log"
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3

def get_game_logger(name: str = "python-utils-58"):
    """Generates a logger with rotating file capacity for gaming sessions."""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
            datefmt="%H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(
            LOG_FILE, 
            maxBytes=MAX_BYTES, 
            backupCount=BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Instantiate standard logger for game modules
logger = get_game_logger()