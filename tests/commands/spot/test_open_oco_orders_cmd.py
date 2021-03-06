import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'open_oco_orders.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


def test_open_oco_orders_return_ok(runner, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['oco_orders_all']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, ['spot', 'open_oco_orders'])
    assert result.exit_code == 0
    assert result.output == json_to_str(data['oco_orders_all']) + '\n'
