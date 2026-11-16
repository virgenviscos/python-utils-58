import logging
from logging.handlers import RotatingFileHandler
import os

def setup_game_logger(name='gaming_engine', log_file='engine.log'):
    """
    Orchestrates the logging flow for the gaming framework.
    Wraps the standard library with a twist for high-frequency writes.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Ensuring the path exists, because games have messy folders
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Rotating handler: 5MB per file, keep 3 backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    
    # Custom formatter for gaming context
    formatter = logging.Formatter(
        '[%(asctime)s][%(levelname)s][TICK:%(process)d] %(message)s',
        datefmt='%H:%M:%S'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Stream output for console debugging
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Initialize with global scope for engine use
game_log = setup_game_logger()