from unittest.mock import Mock

import pytest
from click import BadParameter
from click.testing import CliRunner

from src.commands.cmd_spot import account_info, cli, new_order, open_orders
from src.utils.utils import json_to_str


@pytest.fixture
def runner():
    return CliRunner()


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


def test_cli_root_is_ok(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_new_order_root_is_ok(runner):
    result = runner.invoke(new_order)
    assert result.exit_code == 0


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


def test_account_info_is_ok(runner, mocker):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_account_info()

    mocker.patch('src.builder.get_secret_key', return_value='SECRET_KEY')
    mocker.patch('src.builder.get_api_key_header', return_value={'X-MBX-APIKEY': 'API_KEY'})
    mocker.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(account_info)

    assert result.exit_code == 0
    assert result.output == json_to_str(get_account_info()) + '\n'

