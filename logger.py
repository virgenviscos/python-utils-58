import logging
import time

class GameLogger:
    def __init__(self, name='GameLogger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('game.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_event(self, event, level=logging.INFO):
        if level == logging.DEBUG:
            self.logger.debug(event)
        elif level == logging.WARNING:
            self.logger.warning(event)
        elif level == logging.ERROR:
            self.logger.error(event)
        else:
            self.logger.info(event)

    def log_performance(self, function):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = function(*args, **kwargs)
            end_time = time.time()
            self.logger.info(f'Performance: {function.__name__} executed in {end_time - start_time:.4f} seconds')
            return result
        return wrapper

logger = GameLogger()  

@logger.log_performance
def example_game_loop():
    time.sleep(1)  # Simulate game processing time
    logger.log_event('Game loop executed')

example_game_loop()  
