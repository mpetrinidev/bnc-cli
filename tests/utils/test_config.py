import pytest
import os

from click import FileError

from src.exceptions import ConfigException
from src.utils.config import write_credentials
from src.utils.config import read_credentials
from src.utils.config import get_config_parser
from src.utils.config import get_bnc_config_file_path
from src.utils.config import SECTION


@pytest.fixture()
def mocked_bnc_config_path(mocker):
    mocker.patch('src.utils.config.get_bnc_config_path', return_value=get_bnc_test_config_path())


def get_bnc_test_config_path():
    return os.path.join(os.path.expanduser("~"), '.bnc-tests')


def remove_credentials_file():
    if os.path.isfile(get_bnc_config_file_path()):
        os.remove(get_bnc_config_file_path())


def test_write_credentials_api_key_is_empty(mocked_bnc_config_path):
    with pytest.raises(ValueError, match='api_key cannot be empty'):
        write_credentials('', 'secret')


def test_write_credentials_secret_is_empty(mocked_bnc_config_path):
    with pytest.raises(ValueError, match='secret cannot be empty'):
        write_credentials('api_key', '')


def test_write_credentials_is_ok(mocked_bnc_config_path):
    write_credentials('MY_API_KEY', 'MY_SECRET_KEY')
    assert os.path.isfile(get_bnc_config_file_path())

    config_parser = get_config_parser()
    config_parser.read(get_bnc_config_file_path())

    assert config_parser.has_section(SECTION)
    assert config_parser.has_option(SECTION, 'BNC_CLI_API_KEY')
    assert config_parser.has_option(SECTION, 'BNC_CLI_SECRET_KEY')

    section = config_parser[SECTION]

    assert section['BNC_CLI_API_KEY'] == 'MY_API_KEY'
    assert section['BNC_CLI_SECRET_KEY'] == 'MY_SECRET_KEY'

    os.remove(get_bnc_config_file_path())


def test_read_credentials_file_not_found(mocked_bnc_config_path):
    with pytest.raises(FileError, match='Credentials file does not exists'):
        read_credentials()


def test_read_credentials_file_no_section(mocked_bnc_config_path):
    remove_credentials_file()

    config_parser = get_config_parser()
    with open(get_bnc_config_file_path(), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='api_credentials section cannot be found in credentials file'):
        read_credentials()


def test_read_credentials_file_no_api_key_option(mocked_bnc_config_path):
    config_parser = get_config_parser()
    config_parser.add_section('api_credentials')
    config_parser.set(SECTION, 'BNC_CLI_SECRET_KEY', 'MY_SECRET_KEY')

    with open(get_bnc_config_file_path(), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='BNC_CLI_API_KEY cannot be found in credentials file'):
        read_credentials()

    remove_credentials_file()


def test_read_credentials_file_no_secret_option(mocked_bnc_config_path):
    config_parser = get_config_parser()
    config_parser.add_section('api_credentials')
    config_parser.set(SECTION, 'BNC_CLI_API_KEY', 'MY_API_KEY')

    with open(get_bnc_config_file_path(), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='BNC_CLI_SECRET_KEY cannot be found in credentials file'):
        read_credentials()

    remove_credentials_file()


def test_read_credentials_file_is_ok(mocked_bnc_config_path):
    write_credentials('MY_API_KEY', 'MY_SECRET')
    result = read_credentials()

    assert isinstance(result, dict)
    assert result['api_key'] == 'MY_API_KEY'
    assert result['secret'] == 'MY_SECRET'

    remove_credentials_file()
