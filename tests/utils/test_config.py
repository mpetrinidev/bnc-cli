import pytest
import os

from src.utils.config import write_credentials
from src.utils.config import read_credentials
from src.utils.config import config_parser
from src.utils.config import BNC_CONFIG_FILE_PATH
from src.utils.config import BNC_CONFIG_PATH
from src.utils.config import SECTION


def test_write_credentials_api_key_is_empty():
    with pytest.raises(ValueError, match='api_key cannot be empty'):
        write_credentials('', 'secret')


def test_write_credentials_secret_is_empty():
    with pytest.raises(ValueError, match='secret cannot be empty'):
        write_credentials('api_key', '')


def test_write_credentials_is_ok(monkeypatch):
    write_credentials('MY_API_KEY', 'MY_SECRET_KEY')
    assert os.path.isfile(BNC_CONFIG_FILE_PATH)

    config_parser.read(BNC_CONFIG_FILE_PATH)

    assert config_parser.has_section(SECTION)
    assert config_parser.has_option(SECTION, 'BNC_CLI_API_KEY')
    assert config_parser.has_option(SECTION, 'BNC_CLI_SECRET_KEY')

    section = config_parser[SECTION]

    assert section['BNC_CLI_API_KEY'] == 'MY_API_KEY'
    assert section['BNC_CLI_SECRET_KEY'] == 'MY_SECRET_KEY'

    os.remove(BNC_CONFIG_FILE_PATH)


def test_read_credentials_file_not_found():
    if os.path.isfile(BNC_CONFIG_FILE_PATH):
        os.remove(BNC_CONFIG_FILE_PATH)

    with pytest.raises(FileNotFoundError, match='Credentials file does not exists'):
        read_credentials()
