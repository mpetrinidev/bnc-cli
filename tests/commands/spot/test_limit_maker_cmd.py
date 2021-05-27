import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'new_order.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'limit_maker', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621],
    ['spot', 'new_order', 'limit_maker', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621],

    ['spot', 'new_order', 'limit_maker', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-ncoid', 'iuq4RTzy2HHjw0LZp19JoT'],
    ['spot', 'new_order', 'limit_maker', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621,
     '--new_client_order_id', 'iuq4RTzy2HHjw0LZp19JoT'],

    ['spot', 'new_order', 'limit_maker', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-iq', 0.5],
    ['spot', 'new_order', 'limit_maker', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--iceberg_qty', 0.5],

    ['spot', 'new_order', 'limit_maker', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-ncoid', 'iuq4RTzy2HHjw0LZp19JoT',
     '-iq', 0.5],
    ['spot', 'new_order', 'limit_maker', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621,
     '--new_client_order_id', 'iuq4RTzy2HHjw0LZp19JoT', '--iceberg_qty', 0.5]
])
def test_new_order_limit_maker_return_ack_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['limit_maker_ack']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['limit_maker_ack']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'limit_maker', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-nort', 'FULL'],
    ['spot', 'new_order', 'limit_maker', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--new_order_resp_type', 'FULL']
])
def test_new_order_limit_maker_return_full_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['limit_maker_full']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['limit_maker_full']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'limit_maker', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-nort', 'RESULT'],
    ['spot', 'new_order', 'limit_maker', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--new_order_resp_type', 'RESULT']
])
def test_new_order_limit_maker_return_full_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['limit_maker_result']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['limit_maker_result']) + '\n'
