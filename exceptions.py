class CustomError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

# Error handler for division function

def safe_divide(numerator, denominator):
    try:
        if denominator == 0:
            raise CustomError('Denominator cannot be zero')
        return numerator / denominator
    except CustomError as e:
        print(f'Error: {e.message}')
        return None
    except TypeError:
        print('Error: Both numerator and denominator must be numbers')
        return None

# Error handler for file reading

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f'Error: File {file_path} not found')
        return None
    except IOError:
        print('Error: Could not read file')
        return None

# Error handler for JSON parsing

def parse_json(json_string):
    import json
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        print('Error: Invalid JSON string')
        return None
