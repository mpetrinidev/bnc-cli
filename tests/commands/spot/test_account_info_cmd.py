import os
from unittest.mock import Mock

import pytest
from click import BadParameter

from src.commands.cmd_spot import account_info
from src.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'account_info.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("options", [
    ['-lf', 'G'], ['--locked_free', 'G'],
    ['-lf', ''], ['--locked_free', '']
])
def test_account_info_locked_free_incorrect_value(runner, options):
    result = runner.invoke(account_info, options)

    assert result.exit_code == 2
    assert isinstance(result.exception, (BadParameter, SystemExit))


def test_account_info_is_ok(runner, mock_default_deps, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['account_info']

    mock_default_deps.patch('src.builder.requests.get', return_value=mock_response)

    result = runner.invoke(account_info)

    assert result.exit_code == 0
    assert result.output == json_to_str(data['account_info']) + '\n'

