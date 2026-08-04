import time
import requests

class RetryException(Exception):
    pass

def retry_request(url, max_attempts=5, delay=2):
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Return JSON content
        except requests.exceptions.RequestException as e:
            attempts += 1
            if attempts == max_attempts:
                raise RetryException(f'Failed after {max_attempts} attempts') from e
            time.sleep(delay)
            delay *= 2  # Exponential backoff
    return None  # In case all attempts fail
