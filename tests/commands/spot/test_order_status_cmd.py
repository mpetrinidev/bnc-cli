import os
from unittest.mock import Mock

from src.commands.cmd_spot import order_status
from src.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'order_status.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC'],
    ['--symbol', 'LTCBTC']
])
def test_order_status_missing_order_id_or_orig_client_order_id(runner, params):
    result = runner.invoke(order_status, params)

    assert result.exit_code == 0
    assert result.output == 'Either --order_id (-oid) or --orig_client_order_id (-ocoid) must be sent.\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-oid', 44590],
    ['--symbol', 'LTCBTC', '--order_id', 44590],
    ['-sy', 'LTCBTC', '-ocoid', 'oM1oUenAxizVURTgnsG3pU'],
    ['--symbol', 'LTCBTC', '--orig_client_order_id', 'oM1oUenAxizVURTgnsG3pU'],
    ['-sy', 'LTCBTC', '-oid', 44590, '-ocoid', 'oM1oUenAxizVURTgnsG3pU'],
    ['--symbol', 'LTCBTC', '--order_id', 44590, '--orig_client_order_id', 'oM1oUenAxizVURTgnsG3pU']
])
def test_order_status_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['order_status']

    mock_default_deps.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(order_status, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['order_status']) + '\n'
