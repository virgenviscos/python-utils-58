import logging
import sys
import functools

class GameLogger:
    def __init__(self, name="py-utils-58"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(levelname)s | %(message)s'))
        self.logger.addHandler(handler)

    def safe_execute(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (MemoryError, AttributeError, ValueError) as e:
                self.logger.error(f"Critical crash in {func.__name__}: {str(e)}")
                return None
            except Exception:
                self.logger.critical("Unidentified entity intrusion in stack trace")
                return None
        return wrapper

    def log_event(self, event, status="INFO"):
        safe_msg = str(event)[:1024] if event else "null_payload"
        self.logger.info(f"[{status}] {safe_msg}")

instance = GameLogger()
log = instance.log_event
run = instance.safe_execute