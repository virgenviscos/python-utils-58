import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(log_filename='app.log', max_bytes=1000000, backup_count=3):
    logger = logging.getLogger('RotatingLogger')
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = RotatingFileHandler(log_filename, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Example usage
if __name__ == '__main__':
    log = setup_logger()
    log.info('Logger is set up with rotation!')
    for i in range(10000):
        log.debug(f'Debug message number {i}')