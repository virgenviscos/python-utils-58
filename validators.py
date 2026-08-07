import re

class Validator:
    @staticmethod
    def is_email_valid(email: str) -> bool:
        pattern = r'^[\w!#$%&'*+/=?`{|}~^.-]+@[\w.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_phone_valid(phone: str) -> bool:
        pattern = r'\+?1?\d{9,15}'
        return re.match(pattern, phone) is not None

    @staticmethod
    def is_username_valid(username: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.-]{3,20}$'
        return re.match(pattern, username) is not None

    @staticmethod
    def validate_data(data: dict) -> dict:
        results = {
            'email': Validator.is_email_valid(data.get('email', '')),  
            'phone': Validator.is_phone_valid(data.get('phone', '')),  
            'username': Validator.is_username_valid(data.get('username', ''))
        }
        return results

if __name__ == '__main__':
    sample_data = {
        'email': 'example@test.com',
        'phone': '+1234567890',
        'username': 'user_name123'
    }
    print(Validator.validate_data(sample_data))