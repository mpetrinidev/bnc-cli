import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'all_orders.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['spot', 'all_orders', '-sy', 'LTCBTC'],
    ['spot', 'all_orders', '--symbol', 'LTCBTC'],
])
def test_all_orders_return_all(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['all']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['all']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'all_orders', '-sy', 'LTCBTC', '-oid', 37764],
    ['spot', 'all_orders', '--symbol', 'LTCBTC', '--order_id', 37764]
])
def test_all_orders_get_by_order_id(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['match_order_id']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)

    assert result.exit_code == 0
    assert result.output == json_to_str(data['match_order_id']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'all_orders', '-sy', 'LTCBTC', '-st', 1615176222817, '-et', 1615176222818],
    ['spot', 'all_orders', '--symbol', 'LTCBTC', '--start_time', 1615176222817, '--end_time', 1615176222818],
])
def test_all_orders_start_time_and_end_time(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['start_and_end_time']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)

    assert result.exit_code == 0
    assert result.output == json_to_str(data['start_and_end_time']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'all_orders', '-sy', 'LTCBTC', '--query', "[?status=='EXPIRED']"],
    ['spot', 'all_orders', '--symbol', 'LTCBTC', '--query', "[?status=='EXPIRED']"],
])
def test_all_orders_return_all_filter_by_expired(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['all']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['expired']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'all_orders', '-sy', 'LTCBTC', '--query', "[?type=='STOP_LOSS_LIMIT']"],
    ['spot', 'all_orders', '--symbol', 'LTCBTC', '--query', "[?type=='STOP_LOSS_LIMIT']"],
])
def test_all_orders_return_all_filter_by_stop_loss_limit(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['all']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['stop_loss_limit']) + '\n'
