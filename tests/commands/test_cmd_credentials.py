import pytest
from click.testing import CliRunner

from src.commands.cmd_credentials import add, remove


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize("options", [['--api_key', 'API_KEY_VALUE', '--secret', 'SECRET_VALUE'],
                                     ['--api_key', 'API_KEY_VALUE', '-s', 'SECRET_VALUE'],
                                     ['-ak', 'API_KEY_VALUE', '--secret', 'SECRET_VALUE'],
                                     ['-ak', 'API_KEY_VALUE', '-s', 'SECRET_VALUE']])
def test_credentials_add_options_successfully(runner, options):
    result = runner.invoke(add, options)
    assert result.exit_code == 0
    assert result.output == "Binance CLI's credentials added successfully\n"


def test_credentials_remove_successfully(runner):
    result = runner.invoke(remove)
    assert result.output == "Binance CLI's credentials removed successfully. \n\nRe-run <bnc credentials add> to " \
                            "start using again Binance CLI\n"
