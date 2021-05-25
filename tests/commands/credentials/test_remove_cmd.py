from bnc.cli import cli
from tests.commands.common_fixtures import *


def test_credentials_remove_successfully(runner, mocker):
    mocker.patch('bnc.commands.cmd_credentials.remove_credentials', return_value=None)
    result = runner.invoke(cli, ['credentials', 'remove'])
    assert result.output == "Binance CLI's credentials removed successfully. \n\nRe-run <bnc credentials add> to " \
                            "start using again Binance CLI\n"
