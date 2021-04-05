from unittest.mock import Mock

import pytest
from click import BadParameter
from click.testing import CliRunner

from src.commands.cmd_spot import account_info, cli, new_order, limit, market, stop_loss_limit, take_profit_limit, \
    limit_maker, cancel_order, open_orders, cancel_all_orders
from src.utils.utils import json_to_str
from tests.responses.res_spot import get_full_order_limit, get_full_order_market, get_ack_order_stop_loss_limit, \
    get_ack_order_take_profit_limit, get_ack_order_limit_maker, get_account_info, get_cancel_order, get_open_orders, \
    get_cancel_all_orders


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_default_deps(mocker):
    mocker.patch('src.builder.get_secret_key', return_value='SECRET_KEY')
    mocker.patch('src.builder.get_api_key_header', return_value={'X-MBX-APIKEY': 'API_KEY'})

    return mocker


def test_cli_root_is_ok(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_new_order_root_is_ok(runner):
    result = runner.invoke(new_order)
    assert result.exit_code == 0


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-qoq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--quote_order_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-ncoid', 'test'],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--new_client_order_id', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--stop_price', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--iceberg_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-qoq', 0.0, '-ncoid', 'test',
     '-sp', 0.0, '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621,
     '--quote_order_qty', 0.0, '--new_client_order_id', 0.0, '--stop_price', 0.0, '--iceberg_qty', 0.0]
])
def test_new_order_limit_return_full_resp(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_full_order_limit()

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(limit, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_full_order_limit()) + '\n'


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
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-tif', 'GTC'],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--time_in_force', 'GTC'],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-qoq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--quote_order_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-ncoid', 'test'],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--new_client_order_id', 'test'],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-sp', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--stop_price', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--iceberg_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-tif', 'GTC', '-qoq', 0.0, '-p', 0.0, '-ncoid', 'test',
     '-sp', 0.0, '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--time_in_force', 'GTC',
     '--quote_order_qty', 0.0, '--price', 0.0, '--new_client_order_id', 'test', '--stop_price', 0.0,
     '--iceberg_qty', 0.0]
])
def test_new_order_market_return_full_resp(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_full_order_market()

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(market, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_full_order_market()) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010],
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-qoq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--quote_order_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-ncoid', 'test'],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--new_client_order_id', 'test'],
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--iceberg_qty', 0.0],

    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-qoq', 0.0,
     '-ncoid', 'test', '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--quote_order_qty', 0.0,
     '--new_client_order_id', 'test', '--iceberg_qty', 0.0]
])
def test_new_order_stop_loss_limit_return_ack_resp(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_ack_order_stop_loss_limit()

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(stop_loss_limit, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_ack_order_stop_loss_limit()) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-qoq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--quote_order_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-ncoid', 'test'],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--new_client_order_id', 'test'],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--iceberg_qty', 0.0],

    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-qoq', 0.0,
     '-ncoid', 'test', '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--quote_order_qty', 0.0,
     '--new_client_order_id', 'test', '--iceberg_qty', 0.0]
])
def test_new_order_take_profit_limit_return_ack_resp(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_ack_order_take_profit_limit()

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(take_profit_limit, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_ack_order_take_profit_limit()) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-tif', 'GTC'],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--time_in_force', 'GTC'],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-qoq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--quote_order_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-sp', 0.1],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--stop_price', 0.1],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-ncoid', 'test'],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--new_client_order_id', 'test'],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--iceberg_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1, '-p', 0.003621, '-tif', 'GTC', '-qoq', 0.0, '-sp', 0.1, '-ncoid', 'test',
     '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621, '--time_in_force', 'GTC',
     '--quote_order_qty', 0.0, '--stop_price', 0.1, '--new_client_order_id', 'test', '--iceberg_qty', 0.0]
])
def test_new_order_limit_maker_return_ack_resp(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_ack_order_limit_maker()

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(limit_maker, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_ack_order_limit_maker()) + '\n'


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
def test_cancel_order_return_ok(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_cancel_order()

    mock_default_deps.patch('src.builder.requests.delete', return_value=mock_response)

    result = runner.invoke(cancel_order, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_cancel_order()) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC'],
    ['--symbol', 'LTCBTC']
])
def test_cancel_order_missing_order_id_or_orig_client_order_id(runner, params):
    result = runner.invoke(cancel_order, params)

    assert result.exit_code == 0
    assert result.output == 'Either --order_id (-oid) or --orig_client_order_id (-ocoid) must be sent.\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC'],
    ['--symbol', 'LTCBTC']
])
def test_cancel_all_orders_return_ok(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_cancel_all_orders()

    mock_default_deps.patch('src.builder.requests.delete', return_value=mock_response)

    result = runner.invoke(cancel_all_orders, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_cancel_all_orders()) + '\n'


@pytest.mark.parametrize("options", [
    ['-lf', 'G'], ['--locked_free', 'G'],
    ['-lf', ''], ['--locked_free', '']
])
def test_account_info_locked_free_incorrect_value(runner, options):
    result = runner.invoke(account_info, options)

    assert result.exit_code == 2
    assert isinstance(result.exception, (BadParameter, SystemExit))


def test_account_info_is_ok(runner, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_account_info()

    mock_default_deps.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(account_info)

    assert result.exit_code == 0
    assert result.output == json_to_str(get_account_info()) + '\n'


@pytest.mark.parametrize("params", [
    [],
    ['-sy', 'LTCBTC'],
    ['--symbol', 'LTCBTC']
])
def test_open_orders_return_ok(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_open_orders()

    mock_default_deps.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(open_orders, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_open_orders()) + '\n'

