import configparser
import os

from src.exceptions import ConfigException

SECTION = 'api_credentials'


def get_config_parser():
    return configparser.ConfigParser()


def get_bnc_config_path():
    return os.path.join(os.path.expanduser("~"), '.bnc')


def get_bnc_config_file_path():
    return os.path.join(get_bnc_config_path(), 'credentials')


def write_credentials(api_key: str, secret: str):
    if len(api_key) == 0:
        raise ValueError('api_key cannot be empty')

    if len(secret) == 0:
        raise ValueError('secret cannot be empty')

    bnc_config_file_path = get_bnc_config_file_path()

    if not os.path.isfile(bnc_config_file_path):
        os.makedirs(get_bnc_config_path(), exist_ok=True)

    config_parser = get_config_parser()
    config_parser.read(bnc_config_file_path)

    if not config_parser.has_section(SECTION):
        config_parser.add_section(SECTION)

    config_parser.set(SECTION, 'BNC_CLI_API_KEY', api_key)
    config_parser.set(SECTION, 'BNC_CLI_SECRET_KEY', secret)

    with open(bnc_config_file_path, 'w') as f:
        config_parser.write(f)


def exists_config_file():
    return os.path.isfile(get_bnc_config_file_path())


def read_credentials():
    bnc_config_file_path = get_bnc_config_file_path()

    if not exists_config_file():
        raise ConfigException('Credentials file does not exists')

    config_parser = get_config_parser()
    config_parser.read(bnc_config_file_path)

    if not config_parser.has_section(SECTION):
        raise ConfigException("api_credentials section cannot be found in credentials file")

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
    bnc_config_file_path = get_bnc_config_file_path()

    if not exists_config_file():
        return

    config_parser = get_config_parser()
    with open(bnc_config_file_path, "r") as f:
        config_parser.read_file(f)

    config_parser.remove_section(SECTION)

    with open(bnc_config_file_path, "w") as f:
        config_parser.write(f)
