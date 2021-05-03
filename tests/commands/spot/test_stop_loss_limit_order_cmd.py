import os
from unittest.mock import Mock

from bnc.commands.cmd_spot import stop_loss_limit
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'new_order.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.0060, '-sp', 0.0050],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0060, '--stop_price', 0.0050],

    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.0060, '-sp', 0.0050, '-ncoid', 'custom_id'],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0060, '--stop_price', 0.0050, '--new_client_order_id', 'custom_id'],

    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.0060, '-sp', 0.0050, '-iq', 0.5],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0060, '--stop_price', 0.0050, '--iceberg_qty', 0.5]
])
def test_new_order_stop_loss_limit_return_ack_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['stop_loss_limit_ack']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(stop_loss_limit, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['stop_loss_limit_ack']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.0060, '-sp', 0.0050, '-nort', 'FULL'],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0060, '--stop_price', 0.0050, '--new_order_resp_type', 'FULL'],
])
def test_new_order_stop_loss_limit_return_full_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['stop_loss_limit_full']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(stop_loss_limit, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['stop_loss_limit_full']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.0060, '-sp', 0.0050, '-nort', 'RESULT'],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.0060, '--stop_price', 0.0050, '--new_order_resp_type', 'RESULT'],
])
def test_new_order_stop_loss_limit_return_result_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['stop_loss_limit_result']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(stop_loss_limit, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['stop_loss_limit_result']) + '\n'
