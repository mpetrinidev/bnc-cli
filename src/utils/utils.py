import asyncio
from functools import wraps
import configparser
import os

from click import ClickException

BNC_CONFIG_PATH = os.path.expanduser("~") + "/.bnc"
BNC_CONFIG_FILE_PATH = BNC_CONFIG_PATH + "/credentials"
config_parser = configparser.ConfigParser()


def write_credentials_config_file(api_key: str, secret: str):
    config_parser.add_section('api_credentials')
    config_parser.set('api_credentials', 'BNC_CLI_API_KEY', api_key)
    config_parser.set('api_credentials', 'BNC_CLI_SECRET_KEY', secret)

    if not os.path.isfile(BNC_CONFIG_FILE_PATH):
        os.makedirs(BNC_CONFIG_PATH, exist_ok=True)

    with open(BNC_CONFIG_FILE_PATH, 'w') as f:
        config_parser.write(f)


def read_credentials_config_file():
    if not os.path.isfile(BNC_CONFIG_FILE_PATH):
        raise ClickException('Credentials file does not exists')

    config_parser.read(BNC_CONFIG_FILE_PATH)

    if not config_parser.has_section('api_credentials'):
        raise ClickException('api_credentials section cannot be found in credentials file')

    section = config_parser['api_credentials']

    if not config_parser.has_option('api_credentials', 'BNC_CLI_API_KEY'):
        raise ClickException('BNC_CLI_API_KEY cannot be found in credentials file')

    if not config_parser.has_option('api_credentials', 'BNC_CLI_SECRET_KEY'):
        raise ClickException('BNC_CLI_SECRET_KEY cannot be found in credentials file')

    return {
        "api_key": section['BNC_CLI_API_KEY'],
        "secret": section['BNC_CLI_SECRET_KEY']
    }


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def to_query_string_parameters(values: {}) -> str:
    if not values:
        raise ValueError('values cannot be empty')

    return '&'.join(key + '=' + str(val) for key, val in values.items())
