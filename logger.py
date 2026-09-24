import time
import collections
import functools

class AsyncBufferLogger:
    def __init__(self, capacity=100):
        self._buffer = collections.deque(maxlen=capacity)
        self._last_flush = time.perf_counter()
        self._threshold = 0.5

    def log(self, message: str):
        self._buffer.append(f'[{time.time():.4f}] {message}')
        if len(self._buffer) >= self._buffer.maxlen or (time.perf_counter() - self._last_flush) > self._threshold:
            self.flush()

    def flush(self):
        if not self._buffer:
            return
        output = '\n'.join(self._buffer)
        with open('game_engine.log', 'a') as f:
            f.write(output + '\n')
        self._buffer.clear()
        self._last_flush = time.perf_counter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()

def batch_optimized(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        if duration > 0.016:
            print(f'Warning: {func.__name__} took {duration:.4f}s')
        return result
    return wrapper