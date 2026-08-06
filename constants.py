class Constants:
    MAX_RETRIES = 5
    TIMEOUT_SECONDS = 30
    DEFAULT_PAGE_SIZE = 100
    API_ENDPOINT = 'https://api.example.com'

    @staticmethod
    def get_retry_interval(retry_number):
        return min(2 ** retry_number, Constants.TIMEOUT_SECONDS)

    @staticmethod
    def get_default_headers(api_key):
        return {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def get_available_sizes():
        return [10, 25, 50, 100, 200]

    @staticmethod
    def is_valid_page_size(size):
        return size in Constants.get_available_sizes()