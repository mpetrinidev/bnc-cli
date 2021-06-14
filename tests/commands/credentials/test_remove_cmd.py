from bnc.cli import cli
from tests.commands.common_fixtures import *


@pytest.mark.parametrize('command_text,testnet', [('bnc', False), ('bnc_testnet', True)])
def test_credentials_remove_successfully(runner, mocker, command_text, testnet):
    mocker.patch('bnc.commands.cmd_credentials.remove_credentials', return_value=None)
    mocker.patch('bnc.commands.cmd_credentials.read_configuration', return_value={'is_testnet': testnet})

    result = runner.invoke(cli, ['credentials', 'remove'])

    assert result.output == f"Binance CLI's credentials removed successfully. \n\nRe-run " \
                            f"<{command_text} credentials add> to " \
                            "start using again Binance CLI\n"
