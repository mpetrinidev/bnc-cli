from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from src.commands.cmd_market import cli, test, server_time, exchange_info, trades
from src.utils.utils import json_to_str
from tests.responses.res_market import get_exchange_info, get_trades


@pytest.fixture()
def runner():
    return CliRunner()


def test_cli_root_is_ok(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_test_server_is_up_and_running(runner, mocker):
    mock_response = Mock(status_code=200)
    mocker.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(test)
    assert result.exit_code == 0
    assert result.output == 'Binance API is up and running\n'


def test_server_time_is_up_and_running(runner, mocker):
    resp = {
        "serverTime": 1616520189601
    }

    mock_response = Mock(status_code=200)
    mock_response.json.return_value = resp

    mocker.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(server_time)
    assert result.exit_code == 0
    assert result.output == f'Binance API is up and running\n{json_to_str(resp)}\n'


def test_exchange_info_return_values(runner, mocker):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_exchange_info()

    mocker.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(exchange_info)
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(get_exchange_info())}\n'


def test_trades_return_values(runner, mocker):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_trades()

    mocker.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(exchange_info)
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(get_trades())}\n'


@pytest.mark.parametrize("commands,options", [(test, []), (server_time, []),
                                              (exchange_info, []),
                                              (trades, ['--symbol', "LTCBTC", '--limit', 5])])
def test_market_http_get_commands_return_500(runner, mocker, commands, options):
    mock_response = Mock(status_code=500)
    mocker.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(commands, options)
    assert result.exit_code == 0
    assert result.output == "Binance's side internal error has occurred\n"
