import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_positive_integer(value):
    return isinstance(value, int) and value > 0

# A simple dictionary for validation errors
class ValidationError:
    def __init__(self):
        self.errors = []
    
    def add_error(self, message):
        self.errors.append(message)

    def has_errors(self):
        return len(self.errors) > 0


def main_processing_loop(data):
    validator = ValidationError()
    for entry in data:
        email = entry.get('email')
        age = entry.get('age')
        
        if not validate_email(email):
            validator.add_error(f'Invalid email: {email}')
        if not validate_positive_integer(age):
            validator.add_error(f'Invalid age: {age}')
    
    if validator.has_errors():
        raise ValueError(f'Validation errors: {validator.errors}')