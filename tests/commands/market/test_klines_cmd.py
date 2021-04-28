import os
from unittest.mock import Mock

from tests.commands.common_fixtures import *
from bnc.commands.cmd_market import klines
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'klines.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


@pytest.mark.parametrize("params", [
    ['-sy', "LTCBTC", '-i', '1m'],
    ['--symbol', "LTCBTC", '--interval', '1m']
])
def test_klines_return_values(runner, mock_default_deps, data, params):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['klines']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(klines, params)
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(data["klines"])}\n'


@pytest.mark.parametrize("params", [
    ['-sy', "LTCBTC", '-i', '1m', '-st', 1618670280000, '-et', 1618670579999],
    ['--symbol', "LTCBTC", '--interval', '1m', '--start_time', 1618670280000, '--end_time', 1618670579999]
])
def test_klines_start_time_and_end_time(runner, mock_default_deps, data, params):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['klines_st_et']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(klines, params)
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(data["klines_st_et"])}\n'


@pytest.mark.parametrize("params", [
    ['-sy', "LTCBTC", '-i', '1m', '-l', 1],
    ['--symbol', "LTCBTC", '--interval', '1m', '--limit', 1]
])
def test_klines_limit_1(runner, mock_default_deps, data, params):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['klines_limit_1']

    mock_default_deps.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(klines, params)
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(data["klines_limit_1"])}\n'
