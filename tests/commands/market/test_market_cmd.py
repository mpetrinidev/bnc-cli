from unittest.mock import Mock

from tests.commands.common_fixtures import *

from bnc.commands.cmd_market import cli, test, exchange_info, trades, klines, current_avg_price, ticker_24hr, \
    ticker_price, server_time


def test_cli_root_is_ok(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0


@pytest.mark.parametrize("commands,options", [(test, []), (server_time, []),
                                              (exchange_info, []),
                                              (trades, ['--symbol', 'LTCBTC', '--limit', 5]),
                                              (klines, ['--symbol', 'LTCBTC', '--interval', '1m']),
                                              (current_avg_price, ['--symbol', 'LTCBTC']),
                                              (ticker_24hr, ['--symbol', 'LTCBTC']),
                                              (ticker_price, ['--symbol', 'LTCBTC'])])
def test_market_http_get_commands_return_500(runner, mock_default_deps, commands, options):
    mock_response = Mock(status_code=500, headers={})
    mock_response.json.return_value = None
    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(commands, options)
    assert result.exit_code == 0
    assert result.output == "Binance's side internal error has occurred\n"
