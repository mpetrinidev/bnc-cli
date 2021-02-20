import hashlib
import hmac
import os


from src.exceptions import SecurityException, ConfigException
from src.utils.config import read_credentials


def get_hmac_hash(total_params: str, secret: str) -> str:
    if len(total_params) == 0:
        raise ValueError('total_params cannot be empty')

    if len(secret) == 0:
        raise ValueError('secret cannot be empty')

    signature = hmac.new(str.encode(secret), str.encode(total_params), hashlib.sha256).hexdigest()
    return signature


def get_api_key():
    api_key = os.environ.get('BNC_CLI_API_KEY')

    # Check env variable
    if api_key is None:
        try:
            config_values = read_credentials()
            api_key = config_values['api_key']
        except ConfigException:
            pass

    # Check config file variable
    if api_key is None or len(api_key) == 0:
        raise SecurityException('api_key cannot be null or empty')

    return api_key


def get_secret_key():
    secret_key = os.environ.get('BNC_CLI_SECRET_KEY')

    # Check env variable
    if secret_key is None:
        try:
            config_values = read_credentials()
            secret_key = config_values['secret']
        except ConfigException:
            pass

    # Check config file variable
    if secret_key is None or len(secret_key) == 0:
        raise SecurityException('secret cannot be null or empty')

    return secret_key


def get_api_key_header():
    return {'X-MBX-APIKEY': get_api_key()}
