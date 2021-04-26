from bnc.commands.cmd_credentials import add
from tests.commands.common_fixtures import *


@pytest.mark.parametrize("options", [['--api_key', 'API_KEY_VALUE', '--secret', 'SECRET_VALUE'],
                                     ['--api_key', 'API_KEY_VALUE', '-s', 'SECRET_VALUE'],
                                     ['-ak', 'API_KEY_VALUE', '--secret', 'SECRET_VALUE'],
                                     ['-ak', 'API_KEY_VALUE', '-s', 'SECRET_VALUE']])
def test_credentials_add_options_successfully(runner, options, mocker):
    mocker.patch('bnc.commands.cmd_credentials.write_credentials', return_value=None)
    result = runner.invoke(add, options)
    assert result.exit_code == 0
    assert result.output == "Binance CLI's credentials added successfully\n"
