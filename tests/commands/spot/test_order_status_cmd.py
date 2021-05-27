import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'order_status.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['spot', 'order_status', '-sy', 'LTCBTC'],
    ['spot', 'order_status', '--symbol', 'LTCBTC']
])
def test_order_status_missing_order_id_or_orig_client_order_id(runner, params, mock_default_deps):
    result = runner.invoke(cli, params)

    assert result.exit_code == 0
    assert result.output == 'Either --order_id (-oid) or --orig_client_order_id (-ocoid) must be sent.\n'


@pytest.mark.parametrize("params", [
    ['spot', 'order_status', '-sy', 'LTCBTC', '-oid', 44590],
    ['spot', 'order_status', '--symbol', 'LTCBTC', '--order_id', 44590],
    ['spot', 'order_status', '-sy', 'LTCBTC', '-ocoid', 'oM1oUenAxizVURTgnsG3pU'],
    ['spot', 'order_status', '--symbol', 'LTCBTC', '--orig_client_order_id', 'oM1oUenAxizVURTgnsG3pU'],
    ['spot', 'order_status', '-sy', 'LTCBTC', '-oid', 44590, '-ocoid', 'oM1oUenAxizVURTgnsG3pU'],
    ['spot', 'order_status', '--symbol', 'LTCBTC', '--order_id', 44590, '--orig_client_order_id', 'oM1oUenAxizVURTgnsG3pU']
])
def test_order_status_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['order_status']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['order_status']) + '\n'
