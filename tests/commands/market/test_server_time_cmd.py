from unittest.mock import Mock

from bnc.commands.cmd_market import server_time
from bnc.utils.utils import json_to_str
from tests.commands.common_fixtures import *


def test_server_time_is_up_and_running(runner, mocker):
    resp = {
        "serverTime": 1616520189601
    }

    mock_response = Mock(status_code=200)
    mock_response.json.return_value = resp

    mocker.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(server_time)
    assert result.exit_code == 0
    assert result.output == f'Binance API is up and running\n{json_to_str(resp)}\n'
