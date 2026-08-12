import re

class ValidationError(Exception):
    pass

def validate_username(username):
    if not isinstance(username, str):
        raise ValidationError('Username must be a string')
    if len(username) < 3 or len(username) > 20:
        raise ValidationError('Username must be between 3 and 20 characters')
    if not re.match('^[a-zA-Z0-9_]+$', username):
        raise ValidationError('Username can only contain letters, numbers, and underscores')
    return True

# Example Usage
if __name__ == '__main__':
    usernames = ['valid_user', 'us', 'user_with_special@char', 12345, 'toolongusernamebeyondtwenty']
    for username in usernames:
        try:
            validate_username(username)
            print(f'Username "{username}" is valid.')
        except ValidationError as e:
            print(f'Username "{username}" is invalid: {e}')