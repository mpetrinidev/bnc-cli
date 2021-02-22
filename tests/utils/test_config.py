import pytest
import os

from src.exceptions import ConfigException
from src.utils import config
from src.utils.config import write_credentials
from src.utils.config import read_credentials
from src.utils.config import get_config_parser
from src.utils.config import BNC_CONFIG_FILE_PATH
from src.utils.config import SECTION

config.BNC_CONFIG_PATH = os.path.expanduser("~") + "/.bnc-test"


def remove_credentials_file():
    if os.path.isfile(BNC_CONFIG_FILE_PATH):
        os.remove(BNC_CONFIG_FILE_PATH)


def test_write_credentials_api_key_is_empty():
    with pytest.raises(ValueError, match='api_key cannot be empty'):
        write_credentials('', 'secret')


def test_write_credentials_secret_is_empty():
    with pytest.raises(ValueError, match='secret cannot be empty'):
        write_credentials('api_key', '')


def test_write_credentials_is_ok():
    write_credentials('MY_API_KEY', 'MY_SECRET_KEY')
    assert os.path.isfile(BNC_CONFIG_FILE_PATH)

    config_parser = get_config_parser()
    config_parser.read(BNC_CONFIG_FILE_PATH)

    assert config_parser.has_section(SECTION)
    assert config_parser.has_option(SECTION, 'BNC_CLI_API_KEY')
    assert config_parser.has_option(SECTION, 'BNC_CLI_SECRET_KEY')

    section = config_parser[SECTION]

    assert section['BNC_CLI_API_KEY'] == 'MY_API_KEY'
    assert section['BNC_CLI_SECRET_KEY'] == 'MY_SECRET_KEY'

    os.remove(BNC_CONFIG_FILE_PATH)


def test_read_credentials_file_not_found():
    with pytest.raises(FileNotFoundError, match='Credentials file does not exists'):
        read_credentials()


def test_read_credentials_file_no_section():
    remove_credentials_file()

    config_parser = get_config_parser()
    with open(BNC_CONFIG_FILE_PATH, 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='api_credentials section cannot be found in credentials file'):
        read_credentials()


def test_read_credentials_file_no_api_key_option():
    config_parser = get_config_parser()
    config_parser.add_section('api_credentials')
    config_parser.set(SECTION, 'BNC_CLI_SECRET_KEY', 'MY_SECRET_KEY')

    with open(BNC_CONFIG_FILE_PATH, 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='BNC_CLI_API_KEY cannot be found in credentials file'):
        read_credentials()

    remove_credentials_file()


def test_read_credentials_file_no_secret_option():
    config_parser = get_config_parser()
    config_parser.add_section('api_credentials')
    config_parser.set(SECTION, 'BNC_CLI_API_KEY', 'MY_API_KEY')

    with open(BNC_CONFIG_FILE_PATH, 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='BNC_CLI_SECRET_KEY cannot be found in credentials file'):
        read_credentials()

    remove_credentials_file()


def test_read_credentials_file_is_ok():
    write_credentials('MY_API_KEY', 'MY_SECRET')
    result = read_credentials()

    assert isinstance(result, dict)
    assert result['api_key'] == 'MY_API_KEY'
    assert result['secret'] == 'MY_SECRET'

    remove_credentials_file()
