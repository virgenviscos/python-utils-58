import functools

def validate_game_input(expected_types):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for name, expected in expected_types.items():
                val = kwargs.get(name)
                if val is not None and not isinstance(val, expected):
                    raise TypeError(f'Input {name} expects {expected}, got {type(val)}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

class InputProcessor:
    def __init__(self):
        self.schema = {'x': int, 'y': int, 'action': str}

    def safe_execute(self, command_data):
        try:
            self._process(**command_data)
        except (TypeError, ValueError) as e:
            print(f'rejected malformed packet: {e}')

    @validate_game_input({'x': int, 'y': int, 'action': str})
    def _process(self, **data):
        print(f'executing {data.get("action")} at ({data.get("x")}, {data.get("y")})')

if __name__ == '__main__':
    proc = InputProcessor()
    proc.safe_execute({'x': 10, 'y': 20, 'action': 'move'})
    proc.safe_execute({'x': 'invalid', 'y': 20, 'action': 'jump'})