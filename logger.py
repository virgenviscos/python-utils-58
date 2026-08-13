import logging

class GameLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('game.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def validate_input(self, user_input):
        if not isinstance(user_input, str):
            raise ValueError('Input must be a string')
        if len(user_input) == 0:
            raise ValueError('Input cannot be empty')
        return True

    def process_input(self, user_input):
        self.validate_input(user_input)
        self.log_info(f'Processing input: {user_input}')
        # simulate further processing
        result = f'Processed: {user_input}'
        return result 

if __name__ == '__main__':
    logger = GameLogger('GameLogger')
    try:
        user_input = 'Sample input'
        logger.process_input(user_input)
    except ValueError as e:
        logger.log_error(str(e))