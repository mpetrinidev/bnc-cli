import datetime
import os
from unittest.mock import Mock

from bnc.cli import cli
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file, get_headers
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'account_info.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


def test_account_info_is_ok(runner, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['account_info']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, ['spot', 'account_info'])

    assert result.exit_code == 0
    assert result.output == json_to_str(data['account_info']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'account_info', '--query', 'balances[?to_number(free)>`0.0`] | { balances: @ }']
])
def test_account_info_only_free_balances(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['account_info']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)

    assert result.exit_code == 0
    assert result.output == json_to_str(data['balances_filter_1']) + '\n'


@pytest.mark.parametrize("params", [
    ['spot', 'account_info', '--query', 'balances[?to_number(locked)>`0.0`] | { balances: @ }']
])
def test_account_info_only_locked_balances(runner, params, mock_default_deps, data):
    mock_response = Mock(status_code=200, elapsed=datetime.datetime.now(), headers=get_headers())
    mock_response.json.return_value = data['account_info']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(cli, params)

    assert result.exit_code == 0
    assert result.output == json_to_str(data['balances_filter_2']) + '\n'
