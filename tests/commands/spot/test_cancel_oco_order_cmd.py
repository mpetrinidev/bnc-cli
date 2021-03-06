import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'cancel_oco_order.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['spot', 'cancel_oco_order', '-sy', "LTCBTC", '-olid', 578, '-ncoid', "tKTpu9lI1BjNq8vmnNjtsM"],
    ['spot', 'cancel_oco_order', '--symbol', "LTCBTC", '--order_list_id', 578, '--new_client_order_id', "tKTpu9lI1BjNq8vmnNjtsM"]
])
def test_cancel_oco_order_olid_ncoid_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['cancel_oco_order_olid_ncoid']

    mock_default_deps.patch('bnc.builder.requests.delete', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['cancel_oco_order_olid_ncoid']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'cancel_oco_order', '-sy', "LTCBTC", '-lcoid', "QEOBf6o3NyCf2w6jfj1mrP"],
    ['spot', 'cancel_oco_order', '--symbol', "LTCBTC", '--list_client_order_id', "QEOBf6o3NyCf2w6jfj1mrP"]
])
def test_cancel_oco_order_lcoid_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['cancel_oco_order_lcoid']

    mock_default_deps.patch('bnc.builder.requests.delete', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['cancel_oco_order_lcoid']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'cancel_oco_order', '-sy', "LTCBTC"],
    ['spot', 'cancel_oco_order', '--symbol', "LTCBTC"]
])
def test_cancel_oco_without_lcoid_or_olid_return_error_msg(runner, params, mock_default_deps, data):
    result = runner.invoke(cli, params)

    assert result.exit_code == 0
    assert result.output == 'Either --order_list_id (-olid) or --list_client_order_id (-lcoid) must be sent.\n'
