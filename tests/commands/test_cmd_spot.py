import pytest
from click import BadParameter
from click.testing import CliRunner

from src.commands.cmd_spot import account_info
from src.commands.cmd_spot import validate_recv_window
from src.commands.cmd_spot import validate_locked_free


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize("options", [
    ['-rw', 60001], ['--recv_window', 60001],
    ['-rw', None], ['--recv_window', None],
    ['-rw', 'Incorrect_Value'], ['--recv_window', 'Incorrect_Value']
])
def test_validate_account_info_recv_window_greater_than_60000(runner, options):
    result = runner.invoke(account_info, options)

    assert result.exit_code == 2
    assert isinstance(result.exception, (BadParameter, SystemExit))


@pytest.mark.parametrize("options", [
    ['-lf', 'G'], ['--locked_free', 'G'],
    ['-lf', ''], ['--locked_free', ''],
    ['-lf', None], ['--locked_free', None]
])
def test_validate_account_info_locked_free_incorrect_value(runner, options):
    result = runner.invoke(account_info, options)

    assert result.exit_code == 2
    assert isinstance(result.exception, (BadParameter, SystemExit))


def test_validate_recv_window_greater_than_6000():
    with pytest.raises(BadParameter, match='60001. Cannot exceed 60000'):
        validate_recv_window(None, None, 60001)


def test_validate_locked_free_incorrect_value():
    with pytest.raises(BadParameter, match='G. Possible values: L | F | B'):
        validate_locked_free(None, None, 'G')
