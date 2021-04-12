import os
from unittest.mock import Mock

from src.commands.cmd_spot import new_oco_order
from src.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'new_oco_order.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['-sy', "LTCBTC", '-si', "SELL", '-q', 1, '-p', 0.015, '-sp', 0.008, '-slp', 0.0075, '-sltif', "GTC"],
    ['--symbol', "LTCBTC", '--side', "SELL", '--quantity', 1, '--price', 0.015, '--stop_price', 0.008,
     '--stop_limit_price', 0.0075, '--stop_limit_time_in_force', "GTC"]
])
def test_new_oco_order_return_full_response(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['new_oco_order_full']

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(new_oco_order, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['new_oco_order_full']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', "LTCBTC", '-si', "SELL", '-q', 1, '-p', 0.015, '-sp', 0.008, '-slp', 0.0075, '-sltif', "GTC",
     '-nort', "ACK"],
    ['--symbol', "LTCBTC", '--side', "SELL", '--quantity', 1, '--price', 0.015, '--stop_price', 0.008,
     '--stop_limit_price', 0.0075, '--stop_limit_time_in_force', "GTC", '--new_order_resp_type', "ACK"]
])
def test_new_oco_order_return_ack_response(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['new_oco_order_ack']

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(new_oco_order, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['new_oco_order_ack']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', "LTCBTC", '-si', "SELL", '-q', 1, '-p', 0.015, '-sp', 0.008, '-slp', 0.0075, '-sltif', "GTC",
     '-nort', "RESULT"],
    ['--symbol', "LTCBTC", '--side', "SELL", '--quantity', 1, '--price', 0.015, '--stop_price', 0.008,
     '--stop_limit_price', 0.0075, '--stop_limit_time_in_force', "GTC", '--new_order_resp_type', "RESULT"]
])
def test_new_oco_order_return_result_response(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['new_oco_order_result']

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(new_oco_order, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['new_oco_order_result']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', "LTCBTC", '-si', "SELL", '-q', 1, '-p', 0.015, '-sp', 0.008, '-slp', 0.0075, '-sltif', "GTC",
     '-lcoid', "custom1_list_client_order_id", '-limcoid', "custom_limit_client_order_id",
     '-scoid', "custom_stop_client_order_id"],

    ['--symbol', "LTCBTC", '--side', "SELL", '--quantity', 1, '--price', 0.015, '--stop_price', 0.008,
     '--stop_limit_price', 0.0075, '--stop_limit_time_in_force', "GTC",
     '--list_client_order_id', "custom1_list_client_order_id",
     '--limit_client_order_id', "custom_limit_client_order_id",
     '--stop_client_order_id', "custom_stop_client_order_id"]
])
def test_new_oco_order_set_multiple_custom_ids(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['new_oco_order_custom_ids']

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(new_oco_order, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['new_oco_order_custom_ids']) + '\n'


@pytest.mark.parametrize("params", [
    ['-sy', "LTCBTC", '-si', "SELL", '-q', 1, '-p', 0.015, '-sp', 0.008, '-slp', 0.0075, '-sltif', "GTC",
     '-liq', 0.5, '-siq', 0.5],

    ['--symbol', "LTCBTC", '--side', "SELL", '--quantity', 1, '--price', 0.015, '--stop_price', 0.008,
     '--stop_limit_price', 0.0075, '--stop_limit_time_in_force', "GTC",
     '--limit_iceberg_qty', 0.5, '--stop_iceberg_qty', 0.5]
])
def test_new_oco_order_set_iceberg_qty(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['new_oco_order_iceberg_qty']

    mock_default_deps.patch('src.builder.requests.post', return_value=mock_response)

    result = runner.invoke(new_oco_order, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['new_oco_order_iceberg_qty']) + '\n'
