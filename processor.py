import logging

class InputProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_command(self, cmd_data):
        if not isinstance(cmd_data, dict):
            raise ValueError("invalid data structure")
        
        required = {'action', 'payload'}
        if not required.issubset(cmd_data.keys()):
            raise KeyError(f"missing keys: {required - cmd_data.keys()}")
            
        if not isinstance(cmd_data['action'], str):
            raise TypeError("action must be string")
        return True

    def process_loop(self, queue):
        while True:
            item = queue.get()
            if item is None:
                break
            
            try:
                if self.validate_command(item):
                    self.execute(item['action'], item['payload'])
            except (ValueError, KeyError, TypeError) as e:
                self.logger.warning(f"validation failure: {e}")
                continue

    def execute(self, action, payload):
        # Niche gaming logic: perform state transformation
        state_map = {'move': 0x01, 'jump': 0x02, 'attack': 0x03}
        opcode = state_map.get(action, 0x00)
        if opcode:
            print(f"Executing {action} with {payload}")