import os
from unittest.mock import Mock

from bnc.commands.cmd_spot import my_trades
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'my_trades.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC'],
    ['--symbol', 'LTCBTC'],
])
def test_my_trades_return_all(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['all']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(my_trades, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['all']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-fid', 114],
    ['--symbol', 'LTCBTC', '--from_id', 114]
])
def test_my_trades_get_by_from_id(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['from_id']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(my_trades, params)

    assert result.exit_code == 0
    assert result.output == json_to_str(data['from_id']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '--query', '[?to_number(price)<=`0.0030`]'],
    ['--symbol', 'LTCBTC', '--query', '[?to_number(price)<=`0.0030`]']
])
def test_my_trades_filter_price_less_or_equal_than(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['price_less_or_equal']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(my_trades, params)

    assert result.exit_code == 0
    assert result.output == json_to_str(data['price_less_or_equal']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-st', 1617896183262, '-et', 1617896193262],
    ['--symbol', 'LTCBTC', '--start_time', 1617896183262, '--end_time', 1617896193262]
])
def test_my_trades_start_time_and_end_time(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = data['start_and_end_time']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(my_trades, params)

    assert result.exit_code == 0
    assert result.output == json_to_str(data['start_and_end_time']) + '\n'
