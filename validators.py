import re

def is_email_valid(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_phone_number_valid(phone: str) -> bool:
    pattern = r'^\+?[1-9]\d{1,14}$'
    return re.match(pattern, phone) is not None

def is_url_valid(url: str) -> bool:
    pattern = r'^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/\S*)?$'
    return re.match(pattern, url) is not None

def validate_inputs(inputs: dict) -> dict:
    errors = {}
    if 'email' in inputs and not is_email_valid(inputs['email']):
        errors['email'] = 'Invalid email address'
    if 'phone' in inputs and not is_phone_number_valid(inputs['phone']):
        errors['phone'] = 'Invalid phone number'
    if 'url' in inputs and not is_url_valid(inputs['url']):
        errors['url'] = 'Invalid URL'
    return errors
