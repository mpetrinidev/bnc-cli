from unittest.mock import Mock

import bnc.commands.cmd_market
from tests.commands.common_fixtures import *

from bnc.cli import cli


def test_cli_root_is_ok(runner):
    result = runner.invoke(bnc.commands.cmd_market.cli)
    assert result.exit_code == 0


@pytest.mark.parametrize("commands,options", [(cli, ['market', 'test']), (cli, ['market', 'server_time']),
                                              (cli, ['market', 'exchange_info']),
                                              (cli, ['market', 'trades', '--symbol', 'LTCBTC', '--limit', 5]),
                                              (cli, ['market', 'klines', '--symbol', 'LTCBTC', '--interval', '1m']),
                                              (cli, ['market', 'current_avg_price', '--symbol', 'LTCBTC']),
                                              (cli, ['market', 'ticker_24hr', '--symbol', 'LTCBTC']),
                                              (cli, ['market', 'ticker_price', '--symbol', 'LTCBTC'])])
def test_market_http_get_commands_return_500(runner, mock_default_deps, commands, options):
    mock_response = Mock(status_code=500, headers={})
    mock_response.json.return_value = None
    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(commands, options)
    assert result.exit_code == 0
    assert result.output == "Binance's side internal error has occurred\n"
