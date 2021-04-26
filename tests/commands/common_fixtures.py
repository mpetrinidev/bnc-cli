import pytest
from click.testing import CliRunner


@pytest.fixture(scope='session')
def runner():
    return CliRunner()


@pytest.fixture(scope='function')
def mock_default_deps(mocker):
    mocker.patch('bnc.builder.get_secret_key', return_value='SECRET_KEY')
    mocker.patch('bnc.builder.get_api_key_header', return_value={'X-MBX-APIKEY': 'API_KEY'})

    return mocker
