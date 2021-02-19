import hashlib
import hmac
import os

from click import ClickException
from src.utils.config import read_credentials


def get_hmac_hash(total_params: str, secret: str) -> str:
    if len(total_params) == 0:
        raise ClickException('total_params cannot be empty')

    if len(secret) == 0:
        raise ClickException('secret cannot be empty')

    signature = hmac.new(str.encode(secret), str.encode(total_params), hashlib.sha256).hexdigest()
    return signature


def get_api_key_header():
    return {'X-MBX-APIKEY': get_api_key()}


def get_api_key():
    api_key = os.environ.get('BNC_CLI_API_KEY')

    # read from credentials file if it's None
    if api_key is None:
        try:
            config_values = read_credentials()
            api_key = config_values['api_key']
        except:
            pass

    if api_key is None or len(api_key) == 0:
        raise ClickException('api_key cannot be null or empty')

    return api_key


def del_api_key():
    try:
        del os.environ['BNC_CLI_API_KEY']
    except:
        pass


def get_secret_key():
    secret_key = os.environ.get('BNC_CLI_SECRET_KEY')

    if secret_key is None:
        raise ClickException('You must set bnc secret_key to start using the CLI')

    return secret_key


def del_secret_key():
    try:
        del os.environ['BNC_CLI_SECRET_KEY']
    except:
        pass
