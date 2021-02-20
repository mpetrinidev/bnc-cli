import os

import pytest

from src.exceptions import SecurityException
from src.utils.security import get_secret_key
from src.utils.security import get_hmac_hash
from src.utils.security import get_api_key_header
from src.utils.security import get_api_key
from src.utils.config import write_credentials, remove_credentials

API_KEY = 'SET_YOUR_API_KEY'
SECRET_KEY = 'SET_YOUR_SECRET_KEY'
API_KEY_HEADER = {'X-MBX-APIKEY': API_KEY}


def test_get_hmac_hash_total_params_is_empty_string():
    with pytest.raises(ValueError, match='total_params cannot be empty'):
        get_hmac_hash('', 'secret')


def test_get_hmac_hash_secret_is_empty_string():
    with pytest.raises(ValueError, match='secret cannot be empty'):
        get_hmac_hash('total_params', '')


def test_get_hmac_hash_secret_new_signature():
    total_params = "hello_world"
    secret = 'SECRET_KEY_EXAMPLE'

    assert get_hmac_hash(total_params, secret) == '32d322a281bcd36c64af2bc97e13eee974f24ac900fe4dc7b4901f166d72e6cc'


def test_get_api_key_from_env_ok():
    os.environ['BNC_CLI_API_KEY'] = API_KEY
    assert get_api_key() == API_KEY
    del os.environ['BNC_CLI_API_KEY']


def test_get_api_key_from_config_file():
    write_credentials(API_KEY, SECRET_KEY)
    assert get_api_key() == API_KEY
    remove_credentials()


def test_get_api_key_null_or_empty():
    if os.environ.get('BNC_CLI_API_KEY'):
        del os.environ['BNC_CLI_API_KEY']

    remove_credentials()

    with pytest.raises(SecurityException, match='api_key cannot be null or empty'):
        get_api_key()


def test_get_secret_from_env_ok():
    os.environ['BNC_CLI_SECRET_KEY'] = SECRET_KEY
    assert get_secret_key() == SECRET_KEY
    del os.environ['BNC_CLI_SECRET_KEY']


def test_get_secret_from_config_file():
    write_credentials(API_KEY, SECRET_KEY)
    assert get_secret_key() == SECRET_KEY
    remove_credentials()


def test_get_secret_null_or_empty():
    if os.environ.get('BNC_CLI_SECRET_KEY'):
        del os.environ['BNC_CLI_SECRET_KEY']

    remove_credentials()

    with pytest.raises(SecurityException, match='secret cannot be null or empty'):
        get_secret_key()


def test_get_api_key_header_from_env_ok():
    os.environ['BNC_CLI_API_KEY'] = API_KEY
    assert get_api_key_header() == API_KEY_HEADER
    del os.environ['BNC_CLI_API_KEY']


def test_get_api_key_header_from_config_file_ok():
    write_credentials(API_KEY, SECRET_KEY)
    assert get_api_key_header() == API_KEY_HEADER
    remove_credentials()