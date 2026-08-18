import logging
import os

class CustomLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(f'{name}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)
        self.handle_error(message)

    def handle_error(self, message):
        try:
            with open('error_log.txt', 'a') as f:
                f.write(f'ERROR: {message}\n')
        except Exception as e:
            self.logger.critical(f'Failed to write to error_log.txt: {e}')

    def log_edge_case(self, case):
        if case is None:
            self.log_warning('Received None as edge case input')
        elif not isinstance(case, (int, str)):
            self.log_error(f'Invalid case type: {type(case)}')
        else:
            self.log_info(f'Logging edge case: {case}')