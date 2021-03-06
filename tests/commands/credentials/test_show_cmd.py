from bnc.cli import cli
from tests.commands.common_fixtures import *


def test_credentials_show_successfully(runner, mocker):
    mocker.patch('bnc.commands.cmd_credentials.get_api_key', return_value="API_KEY_VALUE")
    mocker.patch('bnc.commands.cmd_credentials.get_secret_key', return_value="SECRET_KEY_VALUE")

    result = runner.invoke(cli, ['credentials', 'show'])

    assert result.exit_code == 0
    assert result.output == "BNC_CLI_API_KEY: API_KEY_VALUE\nBNC_CLI_SECRET_KEY: SECRET_KEY_VALUE\n"
