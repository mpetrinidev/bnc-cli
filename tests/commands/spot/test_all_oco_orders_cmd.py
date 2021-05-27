import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'all_oco_orders.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


def test_all_oco_orders_without_params_ok(runner, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['all_oco_orders_without_params']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, ['spot', 'all_oco_orders'])
    assert result.exit_code == 0
    assert result.output == json_to_str(data['all_oco_orders_without_params']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'all_oco_orders', '-fid', 590],
    ['spot', 'all_oco_orders', '--from_id', 590],
])
def test_all_oco_orders_from_id_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['all_oco_orders_id']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['all_oco_orders_id']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'all_oco_orders', '-st', 1618359398560, '-et', 1618359398567],
    ['spot', 'all_oco_orders', '--start_time', 1618359398560, '--end_time', 1618359398567],
])
def test_all_oco_orders_st_and_et_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['all_oco_orders_st_and_et']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['all_oco_orders_st_and_et']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'all_oco_orders', '-l', 2],
    ['spot', 'all_oco_orders', '--limit', 2]
])
def test_all_oco_orders_limit_ok(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['all_oco_orders_limit']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    assert result.output == json_to_str(data['all_oco_orders_limit']) + '\n'
