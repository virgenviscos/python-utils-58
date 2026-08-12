import re

def validate_username(username):
    if not isinstance(username, str) or not username:
        return False
    return re.match(r'^[a-zA-Z0-9_]{3,15}$', username) is not None


def validate_level(level):
    if not isinstance(level, int) or level < 1 or level > 100:
        return False
    return True


def validate_input(username, level):
    if not validate_username(username):
        return 'Invalid username. It must be 3-15 characters long, using letters, numbers, and underscores.'
    if not validate_level(level):
        return 'Invalid level. It must be an integer between 1 and 100.'
    return True


def main_processing_loop():
    for _ in range(5):  # Simulating 5 user inputs
        username = input('Enter your username: ')
        level = input('Enter your level (1-100): ')
        try:
            level = int(level)
        except ValueError:
            print('Level must be an integer.')
            continue
        validation_result = validate_input(username, level)
        if validation_result is not True:
            print(validation_result)
        else:
            print('Valid input! Proceeding with the game...')