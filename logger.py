import time
import functools
import logging

logger = logging.getLogger('game_net')

def retry_operation(max_attempts=3, delay=1.5, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts, current_delay = 0, delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f'operation failed after {attempts} attempts: {e}')
                        raise
                    logger.warning(f'retry {attempts}/{max_attempts} in {current_delay}s due to {type(e).__name__}')
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(max_attempts=5)
def execute_network_call(payload):
    # simulates volatile connection in game environment
    import random
    if random.random() < 0.7:
        raise ConnectionError('packet loss detected')
    return {'status': 'success', 'data': payload}