import os
from unittest.mock import Mock

from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *
from bnc.commands.cmd_market import exchange_info
from bnc.utils.utils import json_to_str


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'exchange_info.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


def test_exchange_info_return_values(runner, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['exchange_info']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(exchange_info, [])
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(data["exchange_info"])}\n'
