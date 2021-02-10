from src.utils.security import Security


class Credentials:
    def __init__(self):
        self.api_key = None
        self.secret = None

    def add(self, api_key: str, secret: str):
        if api_key is None or len(api_key) == 0:
            raise ValueError('api_key cannot be null or empty')

        if secret is None or len(secret) == 0:
            raise ValueError('secret cannot be null or empty')

        self.api_key = api_key
        self.secret = secret

        Security.set_secret_key(self.secret)
        Security.set_api_key(self.api_key)

    def remove(self):
        Security.del_secret_key()
        Security.del_api_key()

        self.api_key = None
        self.secret = None
