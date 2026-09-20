import logging

class InputProcessor:
    def __init__(self):
        self.valid_commands = {'move', 'attack', 'cast', 'quit'}

    def sanitize_input(self, user_input):
        return user_input.strip().lower()

    def is_valid(self, cmd):
        return cmd in self.valid_commands

    def process_game_loop(self, input_stream):
        for raw_entry in input_stream:
            clean_cmd = self.sanitize_input(raw_entry)
            
            if not clean_cmd:
                continue

            try:
                if not self.is_valid(clean_cmd):
                    raise ValueError(f'illegal maneuver: {clean_cmd}')
                
                yield self.execute_action(clean_cmd)

            except ValueError as e:
                logging.warning(f'ignored invalid action: {e}')
                yield None

    def execute_action(self, cmd):
        return f'executing {cmd} command successfully'

def run_engine(commands):
    proc = InputProcessor()
    for result in proc.process_game_loop(commands):
        if result:
            print(result)

if __name__ == '__main__':
    data = [' move ', 'invalid', 'attack', 'quit']
    run_engine(data)