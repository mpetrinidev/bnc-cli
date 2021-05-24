from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common_fixtures import *


def test_server_time_is_up_and_running(runner, mock_default_deps):
    resp = {
        "serverTime": 1616520189601
    }

    mock_response = Mock(status_code=200, headers={})
    mock_response.json.return_value = resp

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, ['market', 'server_time'])
    assert result.exit_code == 0
    assert result.output == f'Binance API is up and running\n{json_to_str(resp)}\n'
