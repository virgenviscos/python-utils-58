import time
import requests

class NetworkError(Exception):
    pass


def retry_network_call(func, retries=3, delay=2, *args, **kwargs):
    for attempt in range(retries):
        try:
            response = func(*args, **kwargs)
            if response.status_code == 200:
                return response
            raise NetworkError(f'Error: {response.status_code}')
        except (requests.exceptions.RequestException, NetworkError) as e:
            print(f'Attempt {attempt + 1} failed: {e}')
            time.sleep(delay)
    raise Exception('All retry attempts failed')


def get_game_data(url):
    return retry_network_call(requests.get, url=url)

# Example usage:
# response = get_game_data('https://api.example.com/game')
# print(response.json())
