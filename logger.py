import logging
import datetime
from typing import Any

class GamingLogger:
    def __init__(self, name: str = 'pyutils-58'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def log_event(self, event_type: str, data: Any) -> None:
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.logger.info(f'EVENT:{event_type} | DATA:{data} | TS:{timestamp}')

    def critical_fail(self, message: str) -> None:
        self.logger.error(f'!!! CRITICAL GAMING FAILURE: {message} !!!')

    def __call__(self, msg: str) -> None:
        self.logger.debug(f'TRACE: {msg}')

logger = GamingLogger()