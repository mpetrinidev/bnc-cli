import pytest
import os

from bnc.exceptions import ConfigException

from bnc.utils.config import write_credentials_file, read_json_config_file
from bnc.utils.config import get_bnc_config_path
from bnc.utils.config import write_configuration_file
from bnc.utils.config import read_configuration
from bnc.utils.config import GENERAL_CONFIG_SECTION
from bnc.utils.config import API_INFO_SECTION
from bnc.utils.config import read_credentials
from bnc.utils.config import get_config_parser
from bnc.utils.config import get_bnc_config_filename_path
from bnc.utils.config import CREDENTIALS_SECTION


@pytest.fixture()
def mocked_bnc_config_path(mocker):
    mocker.patch('bnc.utils.config.get_bnc_config_path', return_value=get_bnc_test_config_path())
    return mocker


def get_bnc_test_config_path():
    return os.path.join(os.path.expanduser("~"), '.bnc-tests')


def remove_credentials_file():
    if os.path.isfile(get_bnc_config_filename_path('credentials')):
        os.remove(get_bnc_config_filename_path('credentials'))


def remove_configuration_file():
    if os.path.isfile(get_bnc_config_filename_path('configuration')):
        os.remove(get_bnc_config_filename_path('configuration'))


def test_get_bnc_config_path_config_json_file_is_ok():
    bnc_path = '.bnc'
    final_path = get_bnc_config_path()
    assert final_path == os.path.join(os.path.expanduser("~"), str(bnc_path))


def test_get_bnc_config_path_config_json_file_is_none(mocker):
    mocker.patch('bnc.utils.config.read_json_config_file', return_value={})

    with pytest.raises(ConfigException, match='You must set bnc_config_path in config.json'):
        get_bnc_config_path()


def test_get_bnc_config_path_config_json_file_is_empty(mocker):
    mocker.patch('bnc.utils.config.read_json_config_file', return_value={'bnc_config_path': ''})

    with pytest.raises(ConfigException, match='bnc_config_path cannot be null or empty in config.json'):
        get_bnc_config_path()


def test_write_configuration_file_is_testnet_missing(mocker):
    mocker.patch('bnc.utils.config.read_json_config_file', return_value={
        "bnc_config_path": ".bnc",
        "bnc_api_endpoint": "https://api.binance.com"
    })

    with pytest.raises(ConfigException, match='You must set is_testnet in config.json'):
        write_configuration_file()


def test_write_configuration_file_bnc_config_path_missing(mocker):
    mocker.patch('bnc.utils.config.read_json_config_file', return_value={
        "is_testnet": False,
        "bnc_api_endpoint": "https://api.binance.com"
    })

    with pytest.raises(ConfigException, match='You must set bnc_config_path in config.json'):
        write_configuration_file()


def test_write_configuration_file_bnc_config_path_is_empty(mocker):
    mocker.patch('bnc.utils.config.read_json_config_file', return_value={
        "is_testnet": False,
        "bnc_config_path": "",
        "bnc_api_endpoint": "https://api.binance.com"
    })

    with pytest.raises(ConfigException, match='bnc_config_path cannot be null or empty in config.json'):
        write_configuration_file()


def test_write_configuration_file_bnc_api_endpoint_missing(mocker):
    mocker.patch('bnc.utils.config.read_json_config_file', return_value={
        "is_testnet": False,
        "bnc_config_path": ".bnc"
    })

    with pytest.raises(ConfigException, match='You must set bnc_api_endpoint in config.json'):
        write_configuration_file()


def test_write_configuration_file_bnc_api_endpoint_empty(mocker):
    mocker.patch('bnc.utils.config.read_json_config_file', return_value={
        "is_testnet": False,
        "bnc_config_path": ".bnc",
        "bnc_api_endpoint": ""
    })

    with pytest.raises(ConfigException, match='bnc_api_endpoint cannot be null or empty in config.json'):
        write_configuration_file()


def test_write_configuration_file_is_ok(mocked_bnc_config_path):
    mocked_bnc_config_path.patch('bnc.utils.config.read_json_config_file', return_value={
        "is_testnet": False,
        "bnc_config_path": ".bnc",
        "bnc_api_endpoint": "https://api.binance.com"
    })

    write_configuration_file()

    assert os.path.isfile(get_bnc_config_filename_path('configuration'))

    config_parser = get_config_parser()
    config_parser.read(get_bnc_config_filename_path('configuration'))

    assert config_parser.has_section(GENERAL_CONFIG_SECTION)
    assert config_parser.has_option(GENERAL_CONFIG_SECTION, 'IS_TESTNET')
    assert config_parser.has_option(GENERAL_CONFIG_SECTION, 'BNC_CONFIG_PATH')

    assert config_parser.has_section(API_INFO_SECTION)
    assert config_parser.has_option(API_INFO_SECTION, 'BNC_API_ENDPOINT')

    section = config_parser[GENERAL_CONFIG_SECTION]

    assert section.getboolean('IS_TESTNET') is False
    assert section['BNC_CONFIG_PATH'] == '.bnc'

    section = config_parser[API_INFO_SECTION]

    assert section['BNC_API_ENDPOINT'] == "https://api.binance.com"

    remove_configuration_file()


def test_read_configuration_file_is_ok(mocked_bnc_config_path):
    mocked_bnc_config_path.patch('bnc.utils.config.read_json_config_file', return_value={
        "is_testnet": False,
        "bnc_config_path": ".bnc",
        "bnc_api_endpoint": "https://api.binance.com"
    })

    write_configuration_file()
    config = read_configuration()

    assert config['is_testnet'] is False
    assert config['bnc_config_path'] == '.bnc'
    assert config['bnc_api_endpoint'] == 'https://api.binance.com'

    remove_configuration_file()


def test_read_configuration_file_not_found(mocked_bnc_config_path):
    with pytest.raises(ConfigException, match='Configuration file does not exists'):
        read_configuration()


def test_read_configuration_file_no_general_config_section(mocked_bnc_config_path):
    remove_configuration_file()

    config_parser = get_config_parser()
    with open(get_bnc_config_filename_path('configuration'), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='general section cannot be found in configuration file'):
        read_configuration()

    remove_credentials_file()


def test_read_configuration_file_no_api_info_section(mocked_bnc_config_path):
    remove_configuration_file()

    config_parser = get_config_parser()
    config_parser.add_section(GENERAL_CONFIG_SECTION)
    with open(get_bnc_config_filename_path('configuration'), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='api_info section cannot be found in configuration file'):
        read_configuration()

    remove_credentials_file()


def test_read_configuration_file_is_testnet_option_missing(mocked_bnc_config_path):
    config_parser = get_config_parser()
    config_parser.add_section(GENERAL_CONFIG_SECTION)
    config_parser.add_section(API_INFO_SECTION)

    with open(get_bnc_config_filename_path('configuration'), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException,
                       match='IS_TESTNET cannot be found in configuration file inside general section'):
        read_configuration()

    remove_configuration_file()


def test_read_configuration_file_bnc_config_path_option_missing(mocked_bnc_config_path):
    config_parser = get_config_parser()
    config_parser.add_section(GENERAL_CONFIG_SECTION)
    config_parser.add_section(API_INFO_SECTION)

    config_parser.set(GENERAL_CONFIG_SECTION, 'IS_TESTNET', 'no')

    with open(get_bnc_config_filename_path('configuration'), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException,
                       match='BNC_CONFIG_PATH cannot be found in configuration file inside general section'):
        read_configuration()

    remove_configuration_file()


def test_read_configuration_file_bnc_api_endpoint_option_missing(mocked_bnc_config_path):
    config_parser = get_config_parser()
    config_parser.add_section(GENERAL_CONFIG_SECTION)
    config_parser.add_section(API_INFO_SECTION)

    config_parser.set(GENERAL_CONFIG_SECTION, 'IS_TESTNET', 'no')
    config_parser.set(GENERAL_CONFIG_SECTION, 'BNC_CONFIG_PATH', '.bnc')

    with open(get_bnc_config_filename_path('configuration'), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException,
                       match='BNC_API_ENDPOINT cannot be found in configuration file inside api_info section'):
        read_configuration()

    remove_configuration_file()


def test_write_credentials_api_key_is_empty(mocked_bnc_config_path):
    with pytest.raises(ValueError, match='api_key cannot be empty'):
        write_credentials_file('', 'secret')


def test_write_credentials_secret_is_empty(mocked_bnc_config_path):
    with pytest.raises(ValueError, match='secret cannot be empty'):
        write_credentials_file('api_key', '')


def test_write_credentials_file_is_ok(mocked_bnc_config_path):
    write_credentials_file('MY_API_KEY', 'MY_SECRET_KEY')
    assert os.path.isfile(get_bnc_config_filename_path('credentials'))

    config_parser = get_config_parser()
    config_parser.read(get_bnc_config_filename_path('credentials'))

    assert config_parser.has_section(CREDENTIALS_SECTION)
    assert config_parser.has_option(CREDENTIALS_SECTION, 'BNC_CLI_API_KEY')
    assert config_parser.has_option(CREDENTIALS_SECTION, 'BNC_CLI_SECRET_KEY')

    section = config_parser[CREDENTIALS_SECTION]

    assert section['BNC_CLI_API_KEY'] == 'MY_API_KEY'
    assert section['BNC_CLI_SECRET_KEY'] == 'MY_SECRET_KEY'

    remove_credentials_file()


def test_read_credentials_file_not_found(mocked_bnc_config_path):
    with pytest.raises(ConfigException, match='Credentials file does not exists'):
        read_credentials()


def test_read_credentials_file_no_section(mocked_bnc_config_path):
    remove_credentials_file()

    config_parser = get_config_parser()
    with open(get_bnc_config_filename_path('credentials'), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='api_credentials section cannot be found in credentials file'):
        read_credentials()


def test_read_credentials_file_no_api_key_option(mocked_bnc_config_path):
    config_parser = get_config_parser()
    config_parser.add_section('api_credentials')
    config_parser.set(CREDENTIALS_SECTION, 'BNC_CLI_SECRET_KEY', 'MY_SECRET_KEY')

    with open(get_bnc_config_filename_path('credentials'), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='BNC_CLI_API_KEY cannot be found in credentials file'):
        read_credentials()

    remove_credentials_file()


def test_read_credentials_file_no_secret_option(mocked_bnc_config_path):
    config_parser = get_config_parser()
    config_parser.add_section('api_credentials')
    config_parser.set(CREDENTIALS_SECTION, 'BNC_CLI_API_KEY', 'MY_API_KEY')

    with open(get_bnc_config_filename_path('credentials'), 'w') as f:
        config_parser.write(f)

    with pytest.raises(ConfigException, match='BNC_CLI_SECRET_KEY cannot be found in credentials file'):
        read_credentials()

    remove_credentials_file()


def test_read_credentials_file_is_ok(mocked_bnc_config_path):
    write_credentials_file('MY_API_KEY', 'MY_SECRET')
    result = read_credentials()

    assert isinstance(result, dict)
    assert result['api_key'] == 'MY_API_KEY'
    assert result['secret'] == 'MY_SECRET'

    remove_credentials_file()


def test_read_json_config_file_not_exists(mocker):
    mocker.patch('bnc.utils.config.os.path.join', return_value='')

    with pytest.raises(ConfigException, match='config.json file does not exists'):
        read_json_config_file()
