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


@pytest.mark.parametrize("params", [
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010],
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-qoq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--quote_order_qty', 0.0],
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-ncoid', 'test'],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--new_client_order_id', 'test'],
    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--iceberg_qty', 0.0],

    ['-sy', 'LTCBTC', '-si', 'SELL', '-tif', 'GTC', '-q', 1, '-p', 0.003621, '-sp', 0.0010, '-qoq', 0.0,
     '-ncoid', 'test', '-iq', 0.0],
    ['--symbol', 'LTCBTC', '--side', 'SELL', '--time_in_force', 'GTC',
     '--quantity', 1, '--price', 0.003621, '--stop_price', 0.0010, '--quote_order_qty', 0.0,
     '--new_client_order_id', 'test', '--iceberg_qty', 0.0]
])
def test_new_order_stop_loss_limit_return_ack_resp(runner, params, mock_default_deps):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = get_ack_order_stop_loss_limit()

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(stop_loss_limit, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(get_ack_order_stop_loss_limit()) + '\n'
