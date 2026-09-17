import functools

def validate_game_input(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = args[0] if args else kwargs.get('data')
        if not isinstance(data, dict) or 'action' not in data:
            raise ValueError('invalid game payload structure')
        if data.get('intensity', 0) not in range(0, 11):
            data['intensity'] = 1
        return func(*args, **kwargs)
    return wrapper

class InputProcessor:
    def __init__(self):
        self.history = []

    @validate_game_input
    def process(self, data):
        action = data['action']
        intensity = data.get('intensity', 1)
        result = f'{action} executed at {intensity} power'
        self.history.append(result)
        return result

def run_main_loop(processor, stream):
    for raw_packet in stream:
        try:
            print(processor.process(raw_packet))
        except (ValueError, TypeError) as e:
            print(f'malformed frame ignored: {e}')

if __name__ == '__main__':
    proc = InputProcessor()
    packets = [{'action': 'jump', 'intensity': 5}, {'invalid': 'data'}, {'action': 'run', 'intensity': 99}]
    run_main_loop(proc, packets)