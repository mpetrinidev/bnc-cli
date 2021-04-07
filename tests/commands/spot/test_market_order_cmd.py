import os
from unittest.mock import Mock

from src.commands.cmd_spot import market
from src.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'new_order.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'BUY'],
    ['--symbol', 'LTCBTC', '--side', 'BUY']
])
def test_new_order_market_missing_quantity_or_quote_order_id(runner, params):
    result = runner.invoke(market, params)

    assert result.exit_code == 0
    assert result.output == 'Either --quantity (-q) or --quote_order_qty (-qoq) must be sent.\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1],

    ['-sy', 'LTCBTC', '-si', 'BUY', '-qoq', 0.1],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quote_order_qty', 0.1],

    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-ncoid', 'custom_id'],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--new_client_order_id', 'custom_id'],
])
def test_new_order_market_return_full_resp(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['market_full']

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(market, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['market_full']) + '\n'
