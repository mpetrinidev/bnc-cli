import configparser
import json
import os

from ..exceptions import ConfigException

CREDENTIALS_SECTION = 'api_credentials'
API_INFO_SECTION = 'api_info'
GENERAL_CONFIG_SECTION = 'general'


def get_config_parser():
    return configparser.ConfigParser()


def get_bnc_config_path():
    dic_config = read_json_config_file()
    if 'bnc_config_path' not in dic_config:
        raise ConfigException('You must set bnc_config_path in config.json')

    if len(dic_config['bnc_config_path']) == 0:
        raise ConfigException('bnc_config_path cannot be null or empty in config.json')

    return os.path.join(os.path.expanduser("~"), str(dic_config['bnc_config_path']))


def get_bnc_config_filename_path(filename: str):
    return os.path.join(get_bnc_config_path(), filename)


def exists_config_file(filename: str):
    return os.path.isfile(get_bnc_config_filename_path(filename))


def read_json_config_file():
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')

    if not os.path.isfile(config_file_path):
        raise ConfigException('config.json file does not exists')

    with open(config_file_path) as json_file:
        dic = json.load(json_file)

        return dic


def write_configuration_file():
    dic_config = read_json_config_file()

    if 'is_testnet' not in dic_config:
        raise ConfigException('You must set is_testnet in config.json')

    if 'bnc_config_path' not in dic_config:
        raise ConfigException('You must set bnc_config_path in config.json')

    if len(dic_config['bnc_config_path']) == 0:
        raise ConfigException('bnc_config_path cannot be null or empty in config.json')

    if 'bnc_api_endpoint' not in dic_config:
        raise ConfigException('You must set bnc_api_endpoint in config.json')

    if len(dic_config['bnc_api_endpoint']) == 0:
        raise ConfigException('bnc_api_endpoint cannot be null or empty in config.json')

    configuration_file = get_bnc_config_filename_path('configuration')

    if not os.path.isfile(configuration_file):
        os.makedirs(get_bnc_config_path(), exist_ok=True)

    config_parser = get_config_parser()
    config_parser.read(configuration_file)

    if not config_parser.has_section(GENERAL_CONFIG_SECTION):
        config_parser.add_section(GENERAL_CONFIG_SECTION)

    config_parser.set(GENERAL_CONFIG_SECTION, 'IS_TESTNET', 'yes' if dic_config['is_testnet'] is True else 'no')
    config_parser.set(GENERAL_CONFIG_SECTION, 'BNC_CONFIG_PATH', dic_config['bnc_config_path'])

    if not config_parser.has_section(API_INFO_SECTION):
        config_parser.add_section(API_INFO_SECTION)

    config_parser.set(API_INFO_SECTION, 'BNC_API_ENDPOINT', dic_config['bnc_api_endpoint'])

    with open(configuration_file, 'w') as f:
        config_parser.write(f)


def write_credentials_file(api_key: str, secret: str):
    if len(api_key) == 0:
        raise ValueError('api_key cannot be empty')

    if len(secret) == 0:
        raise ValueError('secret cannot be empty')

    credentials_file = get_bnc_config_filename_path('credentials')

    if not os.path.isfile(credentials_file):
        os.makedirs(get_bnc_config_path(), exist_ok=True)

    config_parser = get_config_parser()
    config_parser.read(credentials_file)

    if not config_parser.has_section(CREDENTIALS_SECTION):
        config_parser.add_section(CREDENTIALS_SECTION)

    config_parser.set(CREDENTIALS_SECTION, 'BNC_CLI_API_KEY', api_key)
    config_parser.set(CREDENTIALS_SECTION, 'BNC_CLI_SECRET_KEY', secret)

    with open(credentials_file, 'w') as f:
        config_parser.write(f)


def read_configuration():
    configuration_file = get_bnc_config_filename_path('configuration')

    if not exists_config_file('configuration'):
        raise ConfigException('Configuration file does not exists')

    config_parser = get_config_parser()
    config_parser.read(configuration_file)

    if not config_parser.has_section(GENERAL_CONFIG_SECTION):
        raise ConfigException("general section cannot be found in configuration file")

    if not config_parser.has_section(API_INFO_SECTION):
        raise ConfigException("api_info section cannot be found in configuration file")

    general_section = config_parser[GENERAL_CONFIG_SECTION]
    api_info_section = config_parser[API_INFO_SECTION]

    if not config_parser.has_option(GENERAL_CONFIG_SECTION, 'IS_TESTNET'):
        raise ConfigException('IS_TESTNET cannot be found in configuration file inside general section')

    if not config_parser.has_option(GENERAL_CONFIG_SECTION, 'BNC_CONFIG_PATH'):
        raise ConfigException('BNC_CONFIG_PATH cannot be found in configuration file inside general section')

    if not config_parser.has_option(API_INFO_SECTION, 'BNC_API_ENDPOINT'):
        raise ConfigException('BNC_API_ENDPOINT cannot be found in configuration file inside api_info section')

    return {
        "is_testnet": general_section.getboolean('IS_TESTNET'),
        "bnc_config_path": general_section['BNC_CONFIG_PATH'],
        "bnc_api_endpoint": api_info_section['BNC_API_ENDPOINT']
    }


def read_credentials():
    credentials_file = get_bnc_config_filename_path('credentials')

    if not exists_config_file('credentials'):
        raise ConfigException('Credentials file does not exists')

    config_parser = get_config_parser()
    config_parser.read(credentials_file)

    if not config_parser.has_section(CREDENTIALS_SECTION):
        raise ConfigException("api_credentials section cannot be found in credentials file")

    section = config_parser[CREDENTIALS_SECTION]

    if not config_parser.has_option(CREDENTIALS_SECTION, 'BNC_CLI_API_KEY'):
        raise ConfigException('BNC_CLI_API_KEY cannot be found in credentials file inside api_credentials section')

    if not config_parser.has_option(CREDENTIALS_SECTION, 'BNC_CLI_SECRET_KEY'):
        raise ConfigException('BNC_CLI_SECRET_KEY cannot be found in credentials file inside api_credentials section')

    return {
        "api_key": section['BNC_CLI_API_KEY'],
        "secret": section['BNC_CLI_SECRET_KEY']
    }


def remove_credentials():
    credentials_file = get_bnc_config_filename_path('credentials')

    if not exists_config_file('credentials'):
        return

    config_parser = get_config_parser()
    with open(credentials_file, "r") as f:
        config_parser.read_file(f)

    config_parser.remove_section(CREDENTIALS_SECTION)

    with open(credentials_file, "w") as f:
        config_parser.write(f)
