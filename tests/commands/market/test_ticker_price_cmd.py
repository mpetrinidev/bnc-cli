import os
from unittest.mock import Mock

from bnc.commands.cmd_market import ticker_price
from bnc.utils.utils import json_to_str
from tests.commands.common import read_json_test_file
from tests.commands.common_fixtures import *


def get_json_filename():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'ticker_price.json')


@pytest.fixture(scope='session')
def data():
    return read_json_test_file(get_json_filename())


def test_ticker_price_return_values(runner, mocker, data):
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = data['ticker_price']

    mocker.patch('bnc.builder.requests.get', return_value=mock_response)

    result = runner.invoke(ticker_price, ['--symbol', 'LTCBTC'])
    assert result.exit_code == 0
    assert result.output == f'{json_to_str(data["ticker_price"])}\n'
