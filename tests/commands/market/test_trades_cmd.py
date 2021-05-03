import os
from unittest.mock import Mock

from tests.commands.common_fixtures import *
from bnc.commands.cmd_market import exchange_info
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'trades.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


def test_trades_return_values(runner, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['trades']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(exchange_info)
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(data["trades"])}\n'
