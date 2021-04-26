import hashlib
import hmac
import os


from ..exceptions import SecurityException, ConfigException
from ..utils.config import read_credentials


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
        raise SecurityException('Credentials are required. Run: bnc credentials add --api_key="your_api_key" '
                                '--secret="your_secret_key" to start using the CLI or add credentials using '
                                'env variables')

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
        raise SecurityException('Credentials are required. Run: bnc credentials add --api_key="your_api_key" '
                                '--secret="your_secret_key" to start using the CLI or add credentials using '
                                'env variables')

    return secret_key


def get_api_key_header():
    return {'X-MBX-APIKEY': get_api_key()}
