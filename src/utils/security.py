import hashlib
import hmac
import os


class Security:
    @staticmethod
    def get_hmac_hash(total_params: str, secret: str) -> str:
        if len(total_params) == 0:
            raise ValueError('total_params cannot be empty')

        if len(secret) == 0:
            raise ValueError('secret cannot be empty')

        signature = hmac.new(str.encode(secret), str.encode(total_params), hashlib.sha256).hexdigest()
        return signature

    @staticmethod
    def get_api_key_header():
        return {'X-MBX-APIKEY': Security.get_api_key()}

    @staticmethod
    def get_api_key():
        try:
            return os.environ['BNC_CLI_API_KEY']
        except Exception:
            raise ValueError('You must set bnc api key to start using the CLI')

    @staticmethod
    def set_api_key(api_key: str):
        if api_key is None:
            return

        os.environ['BNC_CLI_API_KEY'] = api_key

    @staticmethod
    def del_api_key():
        del os.environ['BNC_CLI_API_KEY']

    @staticmethod
    def get_secret_key():
        try:
            return os.environ['BNC_CLI_SECRET_KEY']
        except Exception:
            raise ValueError('You must set bnc secret key to start using the CLI')

    @staticmethod
    def set_secret_key(secret_key: str):
        if secret_key is None:
            return
        os.environ['BNC_CLI_SECRET_KEY'] = secret_key

    @staticmethod
    def del_secret_key():
        del os.environ['BNC_CLI_SECRET_KEY']
