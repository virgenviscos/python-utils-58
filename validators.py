import re

class GameDataValidator:
    @staticmethod
    def validate_username(username):
        if not isinstance(username, str) or len(username) < 3:
            raise ValueError('Username must be a string with at least 3 characters.')
        return True

    @staticmethod
    def validate_score(score):
        if not isinstance(score, int) or score < 0:
            raise ValueError('Score must be a non-negative integer.')
        return True

    @staticmethod
    def validate_email(email):
        email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'  
        if not re.match(email_regex, email):
            raise ValueError('Invalid email format.')
        return True

    @staticmethod
    def validate_game_data(data):
        GameDataValidator.validate_username(data.get('username'))
        GameDataValidator.validate_score(data.get('score'))
        GameDataValidator.validate_email(data.get('email'))
        return True