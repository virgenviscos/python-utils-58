import logging
from logging.handlers import RotatingFileHandler
import os

def get_game_logger(name='python-utils-58', log_file='game_state.log', max_bytes=1048576, backup_count=3):
    """
    A slightly unorthodox logger that treats game logs like a ring buffer
    because nobody likes 50GB of debug trace logs on their SSD.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | [%(levelname)s] | %(message)s')
        
        # File rotation for persistent session history
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        
        # Console output for real-time developer feedback
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Quick access instance
log = get_game_logger()