import logging
from logging.handlers import RotatingFileHandler
import os

class GamingLogger:
    def __init__(self, name='python-utils-58', log_file='game_engine.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | [%(name)s] %(message)s')
        
        # Creative rotating handler: max 5MB, 3 backups
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(handler)
            
        # Console output for dev visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

# Quick access factory
def setup_game_logger(name='python-utils-58'):
    return GamingLogger(name).get_logger()