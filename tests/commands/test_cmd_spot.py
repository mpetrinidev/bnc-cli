from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from src.commands.cmd_spot import cli, new_order, stop_loss_limit, take_profit_limit
from src.utils.utils import json_to_str
from tests.responses.res_spot import get_ack_order_stop_loss_limit, \
    get_ack_order_take_profit_limit


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



