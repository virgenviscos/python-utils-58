import logging
import time

class PerformanceLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_performance(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.logger.debug(f'Executed {func.__name__} in {end_time - start_time:.4f} seconds')
            return result
        return wrapper

@PerformanceLogger('example_logger').log_performance
def sample_function(n):
    total = 0
    for i in range(n):
        total += i
    return total

if __name__ == '__main__':
    sample_function(10000)