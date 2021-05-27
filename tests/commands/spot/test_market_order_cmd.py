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
    ['spot', 'new_order', 'market', '-sy', 'LTCBTC', '-si', 'BUY'],
    ['spot', 'new_order', 'market', '--symbol', 'LTCBTC', '--side', 'BUY']
])
def test_new_order_market_missing_quantity_or_quote_order_id(runner, params, mock_default_deps):
    result = runner.invoke(cli, params)

    assert result.exit_code == 0
    assert result.output == 'Either --quantity (-q) or --quote_order_qty (-qoq) must be sent.\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'market', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1],
    ['spot', 'new_order', 'market', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1],

    ['spot', 'new_order', 'market', '-sy', 'LTCBTC', '-si', 'BUY', '-qoq', 0.1],
    ['spot', 'new_order', 'market', '--symbol', 'LTCBTC', '--side', 'BUY', '--quote_order_qty', 0.1],

    ['spot', 'new_order', 'market', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-ncoid', 'custom_id'],
    ['spot', 'new_order', 'market', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--new_client_order_id',
     'custom_id'],
])
def test_new_order_market_return_full_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['market_full']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['market_full']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'market', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-nort', 'RESULT'],
    ['spot', 'new_order', 'market', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--new_order_resp_type',
     'RESULT']
])
def test_new_order_market_return_result_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['market_result']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['market_result']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'new_order', 'market', '-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-nort', 'ACK'],
    ['spot', 'new_order', 'market', '--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--new_order_resp_type',
     'ACK']
])
def test_new_order_market_return_ack_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['market_ack']

    mock_default_deps.patch('bnc.builder.requests.post', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['market_ack']) + '\n'
