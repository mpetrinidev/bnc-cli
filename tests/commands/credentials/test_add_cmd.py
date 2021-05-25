from bnc.cli import cli
from tests.commands.common_fixtures import *


@pytest.mark.parametrize("options", [['credentials', 'add', '--api_key', 'API_KEY_VALUE', '--secret', 'SECRET_VALUE'],
                                     ['credentials', 'add', '--api_key', 'API_KEY_VALUE', '-s', 'SECRET_VALUE'],
                                     ['credentials', 'add', '-ak', 'API_KEY_VALUE', '--secret', 'SECRET_VALUE'],
                                     ['credentials', 'add', '-ak', 'API_KEY_VALUE', '-s', 'SECRET_VALUE']])
def test_credentials_add_options_successfully(runner, options, mocker):
    mocker.patch('bnc.commands.cmd_credentials.write_credentials_file', return_value=None)
    result = runner.invoke(cli, options)
    assert result.exit_code == 0
    assert result.output == "Binance CLI's credentials added successfully\n"
