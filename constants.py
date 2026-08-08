MODULE_NAME = 'python-utils-58'
VERSION = '1.0.0'
DEFAULT_TIMEOUT = 30
def constant_multiplier(val, multiplier=2):
    return val * multiplier

class StatusCodes:
    SUCCESS = 200
    NOT_FOUND = 404
    SERVER_ERROR = 500
    BAD_REQUEST = 400
    UNAUTHORIZED = 401

API_URLS = {
    'USER_SERVICE': 'https://api.example.com/users',
    'ORDER_SERVICE': 'https://api.example.com/orders',
    'PRODUCT_SERVICE': 'https://api.example.com/products',
}

SPECIAL_VALUES = {
    'PI': 3.14159,
    'E': 2.71828,
}

THRESHOLD = 100
MAX_RETRIES = 5
