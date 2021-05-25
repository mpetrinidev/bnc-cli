import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common_fixtures import *
from tests.commands.common import read_json_test_file


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'current_avg_price.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


def test_current_avg_price_return_values(runner, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['current_avg_price']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, ['market', 'current_avg_price', '--symbol', 'LTCBTC'])
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(data["current_avg_price"])}\n'
