import pytest
from click import BadParameter, ClickException
from click.testing import CliRunner

from src.commands.cmd_spot import account_info


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize("options", [['-rw', 60001], ['--recv_window', 60001]])
def test_validate_account_info_recv_window_greater_than_60000(runner, options):
    result = runner.invoke(account_info, options)

    assert result.exit_code == 2
    assert isinstance(result.exception, (BadParameter, SystemExit))


@pytest.mark.parametrize("options", [['-lf', 'G'], ['--locked_free', 'G'], ['-lf', ''], ['--locked_free', '']])
def test_validate_account_info_locked_free_incorrect_value(runner, options):
    result = runner.invoke(account_info, options)

    assert result.exit_code == 2
    assert isinstance(result.exception, (BadParameter, SystemExit))
