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
        api_key = os.environ.get('BNC_CLI_API_KEY')

        if api_key is None:
            raise ValueError('You must set bnc api_key to start using the CLI')

        return api_key

    @staticmethod
    def set_api_key(api_key: str):
        if len(api_key) == 0:
            raise ValueError('api_key cannot be empty')

        os.environ['BNC_CLI_API_KEY'] = api_key

    @staticmethod
    def del_api_key():
        try:
            del os.environ['BNC_CLI_API_KEY']
        except:
            pass

    @staticmethod
    def get_secret_key():
        secret_key = os.environ.get('BNC_CLI_SECRET_KEY')

        if secret_key is None:
            raise ValueError('You must set bnc secret_key to start using the CLI')

        return secret_key

    @staticmethod
    def set_secret_key(secret_key: str):
        if len(secret_key) == 0:
            raise ValueError('secret_key cannot be empty')

        os.environ['BNC_CLI_SECRET_KEY'] = secret_key

    @staticmethod
    def del_secret_key():
        try:
            del os.environ['BNC_CLI_SECRET_KEY']
        except:
            pass
