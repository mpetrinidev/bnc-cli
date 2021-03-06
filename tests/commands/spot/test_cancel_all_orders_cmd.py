import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'cancel_all_orders.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['spot', 'cancel_all_orders', '-sy', 'LTCBTC'],
    ['spot', 'cancel_all_orders', '--symbol', 'LTCBTC']
])
def test_cancel_all_orders_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['cancel_all_orders']

    mock_default_deps.patch('bnc.builder.requests.delete', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['cancel_all_orders']) + '\n'
