import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'new_order.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'take_profit_limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.0020, '-sp', 0.0015],
    ['spot', 'new_order', 'take_profit_limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0020, '--stop_price', 0.0015],

    ['spot', 'new_order', 'take_profit_limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.0020, '-sp', 0.0015, '-ncoid', 'custom_id'],
    ['spot', 'new_order', 'take_profit_limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0020, '--stop_price', 0.0015, '--new_client_order_id', 'custom_id'],

    ['spot', 'new_order', 'take_profit_limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.0020, '-sp', 0.0015, '-iq', 0.5],
    ['spot', 'new_order', 'take_profit_limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0020, '--stop_price', 0.0015, '--iceberg_qty', 0.5],
])
def test_new_order_take_profit_limit_return_ack_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['take_profit_limit_ack']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['take_profit_limit_ack']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'take_profit_limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.0020, '-sp', 0.0015, '-nort', 'FULL'],
    ['spot', 'new_order', 'take_profit_limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0020, '--stop_price', 0.0015, '--new_order_resp_type', 'FULL'],
])
def test_new_order_take_profit_limit_return_full_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['take_profit_limit_full']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['take_profit_limit_full']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'take_profit_limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.0020, '-sp', 0.0015, '-nort', 'RESULT'],
    ['spot', 'new_order', 'take_profit_limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0020, '--stop_price', 0.0015, '--new_order_resp_type', 'RESULT'],
])
def test_new_order_take_profit_limit_return_result_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['take_profit_limit_result']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['take_profit_limit_result']) + '\n'
