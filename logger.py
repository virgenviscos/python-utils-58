import logging
import os
from logging.handlers import RotatingFileHandler

def get_gaming_logger(name='game_engine', log_file='game.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [LEVEL:%(levelname)s] [MODULE:%(name)s] >> %(message)s',
        datefmt='%H:%M:%S'
    )

    # Unusual approach: size-based rotation with a memory-efficient 1MB limit
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024*1024, 
        backupCount=5
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Console output for real-time development debugging
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Quick patch for immediate usage in the engine
game_logger = get_gaming_logger()