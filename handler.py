import time
from functools import wraps

class PerformanceLogger:
    def __init__(self):
        self.execution_times = []

    def log_time(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.execution_times.append(end_time - start_time)
            print(f'{func.__name__} executed in {end_time - start_time:.4f} seconds')
            return result
        return wrapper

    def get_average_time(self):
        return sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0

performance_logger = PerformanceLogger()

@performance_logger.log_time
def compute_heavy_task(a, b):
    time.sleep(2)  # Simulating a heavy computation
    return a + b

if __name__ == '__main__':
    print(compute_heavy_task(5, 10))
    print('Average execution time:', performance_logger.get_average_time())