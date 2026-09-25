import logging
from logging.handlers import RotatingFileHandler
import os

def setup_game_logger(name: str = 'python-utils-58'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] > %(message)s',
        datefmt='%H:%M:%S'
    )

    log_path = os.path.join(os.getcwd(), 'logs', 'game.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # rotating file handler: 5MB per file, keep 3 backups
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # console output for the impatient developer
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger

logger = setup_game_logger()