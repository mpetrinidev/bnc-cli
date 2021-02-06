import hashlib
import hmac
import os


class Security:
    @staticmethod
    def get_hmac_hash(total_params: str) -> str:
        secret = Security.get_secret_key()

        signature = hmac.new(str.encode(secret), str.encode(total_params), hashlib.sha256).hexdigest()
        return signature

    @staticmethod
    def get_api_key_header():
        return {'X-MBX-APIKEY': Security.get_api_key()}

    @staticmethod
    def get_api_key():
        try:
            return os.environ['BNB_CLI_API_KEY']
        except Exception:
            raise ValueError('You must set bnb api key to start using the CLI')

    @staticmethod
    def set_api_key(api_key: str):
        os.environ['BNB_CLI_API_KEY'] = api_key

    @staticmethod
    def get_secret_key():
        try:
            return os.environ['BNB_CLI_SECRET_KEY']
        except Exception:
            raise ValueError('You must set bnb secret key to start using the CLI')

    @staticmethod
    def set_secret_key(secret_key: str):
        os.environ['BNB_CLI_SECRET_KEY'] = secret_key
