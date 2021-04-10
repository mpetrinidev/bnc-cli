from unittest.mock import Mock
from tests.commands.common_fixtures import *
from src.commands.cmd_market import test


def test_test_server_is_up_and_running(runner, mocker):
    mock_response = Mock(status_code=200)
    mocker.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(test)
    assert result.exit_code == 0
    assert result.output == 'Binance API is up and running\n'
