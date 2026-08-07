class CustomError(Exception):
    """Base class for custom exceptions."""
    pass

class ValidationError(CustomError):
    """Raised for validation errors."""
    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors or []
        super().__init__(self.message)

class ConnectionError(CustomError):
    """Raised for connection-related issues."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotFoundError(CustomError):
    """Raised when a resource is not found."""
    def __init__(self, resource):
        self.message = f'{resource} not found'
        super().__init__(self.message)

def handle_error(error):
    if isinstance(error, ValidationError):
        return {'status': 'error', 'message': error.message, 'details': error.errors}
    elif isinstance(error, ConnectionError):
        return {'status': 'error', 'message': 'Connection issue: ' + error.message}
    elif isinstance(error, NotFoundError):
        return {'status': 'error', 'message': error.message}
    else:
        return {'status': 'error', 'message': 'An unknown error occurred'}
