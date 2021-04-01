import json

import pytest
from click.testing import CliRunner


def read_json_file(name):
    with open(name) as json_file:
        response = json.load(json_file)

        return response


@pytest.fixture(scope='session')
def runner():
    return CliRunner()


@pytest.fixture(scope='function')
def mock_default_deps(mocker):
    mocker.patch('src.builder.get_secret_key', return_value='SECRET_KEY')
    mocker.patch('src.builder.get_api_key_header', return_value={'X-MBX-APIKEY': 'API_KEY'})

    return mocker
