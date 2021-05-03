import os
from unittest.mock import Mock

from bnc.commands.cmd_spot import cancel_order
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'cancel_order.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC'],
    ['--symbol', 'LTCBTC']
])
def test_cancel_order_missing_order_id_or_orig_client_order_id(runner, params):
    result = runner.invoke(cancel_order, params)

    assert result.exit_code == 0
    assert result.output == 'Either --order_id (-oid) or --orig_client_order_id (-ocoid) must be sent.\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-oid', 44590],
    ['--symbol', 'LTCBTC', '--order_id', 44590],
    ['-sy', 'LTCBTC', '-ocoid', 'oM1oUenAxizVURTgnsG3pU'],
    ['--symbol', 'LTCBTC', '--orig_client_order_id', 'oM1oUenAxizVURTgnsG3pU'],
    ['-sy', 'LTCBTC', '-oid', 44590, '-ocoid', 'oM1oUenAxizVURTgnsG3pU'],
    ['--symbol', 'LTCBTC', '--order_id', 44590, '--orig_client_order_id', 'oM1oUenAxizVURTgnsG3pU'],
    ['-sy', 'LTCBTC', '-oid', 44590, '-ocoid', 'oM1oUenAxizVURTgnsG3pU', '-ncoid', 'vmITMP7NPf3EfSmcyzX6JF'],
    ['--symbol', 'LTCBTC', '--order_id', 44590,
     '--orig_client_order_id', 'oM1oUenAxizVURTgnsG3pU',
     '--new_client_order_id', 'vmITMP7NPf3EfSmcyzX6JF'],
])
def test_cancel_order_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['cancel_order']

    mock_default_deps.patch('bnc.builder.requests.delete', return_value=mock_response)

    result = runner.invoke(cancel_order, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['cancel_order']) + '\n'

