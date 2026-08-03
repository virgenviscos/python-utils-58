import math
import string
import random

def generate_random_string(length=10, include_digits=True, include_punctuation=False):
    charset = string.ascii_letters
    if include_digits:
        charset += string.digits
    if include_punctuation:
        charset += string.punctuation
    return ''.join(random.choice(charset) for _ in range(length))


def calculate_square_root(value):
    if value < 0:
        raise ValueError('Cannot compute the square root of a negative number')
    return math.sqrt(value)


def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def factorial(n):
    if n < 0:
        raise ValueError('Factorial is not defined for negative numbers')
    return 1 if n == 0 else n * factorial(n - 1)