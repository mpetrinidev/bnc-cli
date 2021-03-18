from unittest.mock import Mock

import pytest
from click import BadParameter
from click.testing import CliRunner

from src.commands.cmd_spot import account_info, cli, new_order, limit, market, stop_loss_limit, take_profit_limit, \
    limit_maker
from src.utils.utils import json_to_str


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_default_deps(mocker):
    mocker.patch('src.builder.get_secret_key', return_value='SECRET_KEY')
    mocker.patch('src.builder.get_api_key_header', return_value={'X-MBX-APIKEY': 'API_KEY'})

    return mocker


def get_account_info():
    return {
        "makerCommission": 15,
        "takerCommission": 15,
        "buyerCommission": 0,
        "sellerCommission": 0,
        "canTrade": True,
        "canWithdraw": True,
        "canDeposit": True,
        "updateTime": 123456789,
        "accountType": "SPOT",
        "balances": get_balances(),
        "permissions": [
            "SPOT"
        ]
    }


def get_balances():
    return [
        {
            "asset": "BTC",
            "free": "4723846.89208129",
            "locked": "0.00000000"
        },
        {
            "asset": "LTC",
            "free": "4763368.68006011",
            "locked": "0.00000000"
        },
        {
            "asset": "BNB",
            "free": "0.00000000",
            "locked": "10.250"
        }
    ]


def get_full_order_limit():
    return {
        "symbol": "LTCBTC",
        "orderId": 44588,
        "orderListId": -1,
        "clientOrderId": "Xxv5X3sWh6wxIPtlZxkKmS",
        "transactTime": 1616029165071,
        "price": "0.00362100",
        "origQty": "1.00000000",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "NEW",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "side": "BUY",
        "fills": []
    }


def get_full_order_market():
    return {
        "symbol": "LTCBTC",
        "orderId": 44589,
        "orderListId": -1,
        "clientOrderId": "6lcsZpGiMMwCQlwVLtfMXz",
        "transactTime": 1616029239160,
        "price": "0.00000000",
        "origQty": "1.00000000",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "EXPIRED",
        "timeInForce": "GTC",
        "type": "MARKET",
        "side": "BUY",
        "fills": []
    }


def get_ack_order_stop_loss_limit():
    return {
        "symbol": "LTCBTC",
        "orderId": 44590,
        "orderListId": -1,
        "clientOrderId": "oM1oUenAxizVURTgnsG3pU",
        "transactTime": 1616030090950
    }


def get_ack_order_take_profit_limit():
    return {
        "symbol": "LTCBTC",
        "orderId": 44591,
        "orderListId": -1,
        "clientOrderId": "WHnGqkVEOYf6aIcJTuHfJa",
        "transactTime": 1616031609028
    }


def get_ack_order_limit_maker():
    return {
        "symbol": "LTCBTC",
        "orderId": 44592,
        "orderListId": -1,
        "clientOrderId": "iuq4RTzy2HHjw0LZp19JoT",
        "transactTime": 1616031749054
    }


def test_cli_root_is_ok(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_new_order_root_is_ok(runner):
    result = runner.invoke(new_order)
    assert result.exit_code == 0


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'BUY', '-tif', 'GTC', '-q', 1, '-p', 0.003621],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--time_in_force', 'GTC', '--quantity', 1, '--price', 0.003621]
])
def test_new_order_limit_return_full_resp(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_full_order_limit()

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(limit, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_full_order_limit()) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'BUY', '-q', 1],
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1]
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
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010]
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
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010]
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
    ['--symbol', 'LTCBTC', '--side', 'BUY', '--quantity', 1, '--price', 0.003621]
])
def test_new_order_limit_maker_return_ack_resp(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_ack_order_limit_maker()

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(limit_maker, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_ack_order_limit_maker()) + '\n'


@pytest.mark.parametrize("options", [
    ['-rw', 60001], ['--recv_window', 60001],
    ['-rw', 'Incorrect_Value'], ['--recv_window', 'Incorrect_Value']
])
def test_account_info_recv_window_greater_than_60000(runner, options):
    result = runner.invoke(account_info, options)

    assert result.exit_code == 2
    assert isinstance(result.exception, (BadParameter, SystemExit))


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
