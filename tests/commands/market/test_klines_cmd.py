import os
from unittest.mock import Mock

from tests.commands.common_fixtures import *
from src.commands.cmd_market import klines
from src.utils.utils import json_to_str
from tests.commands.common import read_json_test_file


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'klines.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


def test_klines_return_values(runner, mocker, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['klines']

    mocker.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(klines, ['--symbol', 'LTCBTC', '--interval', '1m'])
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(data["klines"])}\n'
