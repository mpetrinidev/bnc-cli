import os

import pytest

from src.exceptions import SecurityException, ConfigException
from src.utils.security import get_secret_key
from src.utils.security import get_hmac_hash
from src.utils.security import get_api_key_header
from src.utils.security import get_api_key
from src.utils.config import write_credentials, remove_credentials

API_KEY = 'SET_YOUR_API_KEY'
SECRET_KEY = 'SET_YOUR_SECRET_KEY'
API_KEY_HEADER = {'X-MBX-APIKEY': API_KEY}


@pytest.fixture()
def mocked_bnc_config_path(mocker):
    mocker.patch('src.utils.config.get_bnc_config_path', return_value=get_bnc_test_config_path())


def get_bnc_test_config_path():
    return os.path.join(os.path.expanduser("~"), '.bnc-tests')


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


def test_get_api_key_from_config_file(mocked_bnc_config_path):
    write_credentials(API_KEY, SECRET_KEY)
    assert get_api_key() == API_KEY
    remove_credentials()


def test_get_api_key_null_or_empty(mocker):
    mocker.patch('os.environ.get', return_value=None)
    mocker.patch('src.utils.security.read_credentials', side_effect=ConfigException('Custom_Exception'))

    with pytest.raises(SecurityException,
                       match='Credentials are required. Run: bnc credentials add --api_key="your_api_key" '
                             '--secret="your_secret_key" to start using the CLI or add credentials using '
                             'env variables'):
        get_api_key()


def test_get_secret_from_env_ok():
    os.environ['BNC_CLI_SECRET_KEY'] = SECRET_KEY
    assert get_secret_key() == SECRET_KEY
    del os.environ['BNC_CLI_SECRET_KEY']


def test_get_secret_from_config_file(mocked_bnc_config_path):
    write_credentials(API_KEY, SECRET_KEY)
    assert get_secret_key() == SECRET_KEY
    remove_credentials()


def test_get_secret_null_or_empty(mocker):
    mocker.patch('os.environ.get', return_value=None)
    mocker.patch('src.utils.security.read_credentials', side_effect=ConfigException('Custom_Exception'))

    with pytest.raises(SecurityException, match='Credentials are required. Run: bnc credentials add '
                                                '--api_key="your_api_key" '
                                                '--secret="your_secret_key" to start using the CLI or add credentials '
                                                'using env variables'):
        get_secret_key()


def test_get_api_key_header_from_env_ok():
    os.environ['BNC_CLI_API_KEY'] = API_KEY
    assert get_api_key_header() == API_KEY_HEADER
    del os.environ['BNC_CLI_API_KEY']


def test_get_api_key_header_from_config_file_ok(mocked_bnc_config_path):
    write_credentials(API_KEY, SECRET_KEY)
    assert get_api_key_header() == API_KEY_HEADER
    remove_credentials()
