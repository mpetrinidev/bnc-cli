import pytest
from click.testing import CliRunner

from src.commands.cmd_credentials import add, remove


@pytest.fixture
def runner():
    return CliRunner()


def test_credentials_add_successfully(runner):
    result = runner.invoke(add, ['API_KEY_VALUE', 'SECRET_VALUE'])
    assert result.output == "Binance CLI's credentials added successfully\n"


def test_credentials_remove_successfully(runner):
    result = runner.invoke(remove)
    assert result.output == "Binance CLI's credentials removed successfully. \n\nRe-run <bnc credentials add> to " \
                            "start using again Binance CLI\n"
