import logging
from logging.handlers import RotatingFileHandler
import os

class GamingLogger:
    def __init__(self, name='game_engine', log_file='engine.log', max_bytes=1048576, backups=5):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
        
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backups)
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
    def get_logger(self):
        return self.logger

def setup_game_logger():
    return GamingLogger().get_logger()

if __name__ == '__main__':
    log = setup_game_logger()
    log.info('System initialized for gaming operations')