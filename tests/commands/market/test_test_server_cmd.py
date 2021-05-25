from unittest.mock import Mock

from bnc.cli import cli
from tests.commands.common_fixtures import *


def test_test_server_is_up_and_running(runner, mock_default_deps):
    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = None
    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, ['market', 'test'])
    assert result.exit_code == 0
    assert result.output == 'Binance API is up and running\n'
