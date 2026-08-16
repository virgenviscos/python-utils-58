import re

def validate_username(username):
    if not isinstance(username, str):
        raise ValueError('Username must be a string')
    if len(username) < 3 or len(username) > 20:
        raise ValueError('Username must be between 3 and 20 characters')
    if not re.match('^[a-zA-Z0-9_]*$', username):
        raise ValueError('Username can only contain letters, numbers, and underscores')
    return True

def validate_score(score):
    if not isinstance(score, int):
        raise ValueError('Score must be an integer')
    if score < 0:
        raise ValueError('Score cannot be negative')
    return True

if __name__ == '__main__':
    usernames = ['player1', 'user@name', 'gamer_99']
    scores = [10, -5, 35]

    for username in usernames:
        try:
            validate_username(username)
            print(f'{username} is valid')
        except ValueError as e:
            print(f'Invalid username: {e}')

    for score in scores:
        try:
            validate_score(score)
            print(f'Score {score} is valid')
        except ValueError as e:
            print(f'Invalid score: {e}')