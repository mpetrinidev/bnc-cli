import configparser
import os

from src.exceptions import ConfigException

BNC_CONFIG_PATH = os.path.expanduser("~") + "/.bnc"
BNC_CONFIG_FILE_PATH = BNC_CONFIG_PATH + "/credentials"
SECTION = 'api_credentials'
config_parser = configparser.ConfigParser()


def write_credentials(api_key: str, secret: str):
    if not os.path.isfile(BNC_CONFIG_FILE_PATH):
        os.makedirs(BNC_CONFIG_PATH, exist_ok=True)

    config_parser.read(BNC_CONFIG_FILE_PATH)

    if not config_parser.has_section(SECTION):
        config_parser.add_section(SECTION)

    config_parser.set(SECTION, 'BNC_CLI_API_KEY', api_key)
    config_parser.set(SECTION, 'BNC_CLI_SECRET_KEY', secret)

    with open(BNC_CONFIG_FILE_PATH, 'w') as f:
        config_parser.write(f)


def read_credentials():
    if not os.path.isfile(BNC_CONFIG_FILE_PATH):
        raise FileNotFoundError('Credentials file does not exists')

    config_parser.read(BNC_CONFIG_FILE_PATH)

    if not config_parser.has_section(SECTION):
        raise ConfigException('api_credentials section cannot be found in credentials file')

    section = config_parser[SECTION]

    if not config_parser.has_option(SECTION, 'BNC_CLI_API_KEY'):
        raise ConfigException('BNC_CLI_API_KEY cannot be found in credentials file')

    if not config_parser.has_option(SECTION, 'BNC_CLI_SECRET_KEY'):
        raise ConfigException('BNC_CLI_SECRET_KEY cannot be found in credentials file')

    return {
        "api_key": section['BNC_CLI_API_KEY'],
        "secret": section['BNC_CLI_SECRET_KEY']
    }


def remove_credentials():
    if not os.path.isfile(BNC_CONFIG_FILE_PATH):
        raise FileNotFoundError('Credentials file does not exists')

    with open(BNC_CONFIG_FILE_PATH, "r") as f:
        config_parser.read_file(f)

    config_parser.remove_section(SECTION)

    with open(BNC_CONFIG_FILE_PATH, "w") as f:
        config_parser.write(f)

