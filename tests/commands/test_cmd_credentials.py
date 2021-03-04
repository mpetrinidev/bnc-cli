import pytest
from click.testing import CliRunner

from src.commands.cmd_credentials import add
from src.commands.cmd_credentials import remove
from src.commands.cmd_credentials import show

from src.utils.config import write_credentials
from src.utils.config import remove_credentials


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


def test_credentials_show_successfully(runner):
    write_credentials("API_KEY_VALUE", "SECRET_KEY_VALUE")

    result = runner.invoke(show)

    assert result.exit_code == 0
    assert result.output == "BNC_CLI_API_KEY: API_KEY_VALUE\nBNC_CLI_SECRET_KEY: SECRET_KEY_VALUE\n"

    remove_credentials()
