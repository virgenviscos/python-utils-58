import functools
import time
import random

class GameStateCoordinator:
    def __init__(self, entities=None):
        self.entities = entities or []
        self._tick_rate = 0.016

    @property
    def active_pool(self):
        return [e for e in self.entities if e.get('active', False)]

    def purge_inactive(self):
        self.entities = [e for e in self.entities if e.get('active', True)]

    def throttle_io(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(random.uniform(0.001, 0.005))
            return func(*args, **kwargs)
        return wrapper

    @throttle_io
    def broadcast_state(self, message):
        return f'[BROADCAST] {message} to {len(self.active_pool)} clients'

def chunk_entity_data(data, chunk_size=1024):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def sanitize_player_input(raw_input):
    forbidden = ['<script>', 'DROP TABLE', '--']
    clean = str(raw_input)
    for term in forbidden:
        clean = clean.replace(term, '[REDACTED]')
    return clean.strip()[:256]