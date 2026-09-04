import logging
from logging.handlers import RotatingFileHandler
import os

class GamingLogger:
    def __init__(self, name='python-utils-58', log_dir='logs'):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(message)s',
            datefmt='%H:%M:%S'
        )

        file_path = os.path.join(log_dir, f'{name}.log')
        handler = RotatingFileHandler(
            file_path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

logger = GamingLogger().get_logger()