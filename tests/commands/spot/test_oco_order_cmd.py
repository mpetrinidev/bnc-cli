import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'oco_order.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['spot', 'oco_order', '-olid', 592, '-lcoid', "ykprg1hXtgmNjHVcZ3YKNM"],
    ['spot', 'oco_order', '--order_list_id', 592, '--list_client_order_id', "ykprg1hXtgmNjHVcZ3YKNM"]
])
def test_oco_order_ocoid_and_lcoid_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['get_oco_order']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['get_oco_order']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'oco_order', '-olid', 592],
    ['spot', 'oco_order', '--order_list_id', 592]
])
def test_oco_order_only_ocoid_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['get_oco_order']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['get_oco_order']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'oco_order', '-lcoid', "ykprg1hXtgmNjHVcZ3YKNM"],
    ['spot', 'oco_order', '--list_client_order_id', "ykprg1hXtgmNjHVcZ3YKNM"]
])
def test_oco_order_only_lcoid_return_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['get_oco_order']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['get_oco_order']) + '\n'


def test_cancel_oco_without_lcoid_or_olid_return_error_msg(runner, mock_default_deps, data):
    result = runner.invoke(cli, ['spot', 'oco_order'])

    assert result.exit_code == 0
    assert result.output == 'Either --order_list_id (-olid) or --list_client_order_id (-lcoid) must be sent.\n'
