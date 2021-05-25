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
    ['spot', 'new_order', 'limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621],
    ['spot', 'new_order', 'limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621],
    ['spot', 'new_order', 'limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-ncoid', "custom_id"],
    ['spot', 'new_order', 'limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--new_client_order_id', "custom_id"],
    ['spot', 'new_order', 'limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-iq', 0.20],
    ['spot', 'new_order', 'limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--iceberg_qty', 0.20]
])
def test_new_order_limit_return_full_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['limit_full']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['limit_full']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-nort', 'ACK'],
    ['spot', 'new_order', 'limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--new_order_resp_type', 'ACK']
])
def test_new_order_limit_return_ack_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['limit_ack']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['limit_ack']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'limit', '-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-nort', 'RESULT'],
    ['spot', 'new_order', 'limit', '--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--new_order_resp_type', 'RESULT']
])
def test_new_order_limit_return_ack_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['limit_result']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['limit_result']) + '\n'
