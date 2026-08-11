import time
import requests
from functools import wraps


def retry(retries=3, delay=2, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt < retries - 1:
                        time.sleep(delay)
                        delay *= backoff  # Increase delay
                    else:
                        raise e  # Reraise the exception after retries are exhausted
        return wrapper
    return decorator


@retry(retries=5, delay=1)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad responses
    return response.json()


if __name__ == '__main__':
    try:
        data = fetch_data('https://api.example.com/data')
        print(data)
    except requests.exceptions.RequestException as e:
        print(f'Network error: {e}')