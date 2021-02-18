import asyncio
from functools import wraps
import configparser
import os

BNC_CONFIG_PATH = os.path.expanduser("~") + "/.bnc"
BNC_CONFIG_FILE_PATH = BNC_CONFIG_PATH + "/credentials"
config = configparser.ConfigParser()


def write_credentials_config_file(api_key: str, secret: str):
    config.add_section('api_credentials')
    config.set('api_credentials', 'BNC_CLI_API_KEY', api_key)
    config.set('api_credentials', 'BNC_CLI_SECRET_KEY', secret)

    if not os.path.isfile(BNC_CONFIG_FILE_PATH):
        os.makedirs(BNC_CONFIG_PATH, exist_ok=True)

    with open(BNC_CONFIG_FILE_PATH, 'w') as f:
        config.write(f)


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def to_query_string_parameters(values: {}) -> str:
    if not values:
        raise ValueError('values cannot be empty')

    return '&'.join(key + '=' + str(val) for key, val in values.items())
