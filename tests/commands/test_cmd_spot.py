import pytest
from click import BadParameter
from click.testing import CliRunner

from src.commands.cmd_spot import account_info
from src.commands.cmd_spot import validate_recv_window
from src.commands.cmd_spot import validate_locked_free
from src.commands.cmd_spot import filter_balances


@pytest.fixture
def runner():
    return CliRunner()


def get_balances():
    return [
        {
            "asset": "BTC",
            "free": "4723846.89208129",
            "locked": "0.00000000"
        },
        {
            "asset": "LTC",
            "free": "4763368.68006011",
            "locked": "0.00000000"
        },
        {
            "asset": "BNB",
            "free": "0.00000000",
            "locked": "10.250"
        }
    ]


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


@pytest.mark.parametrize("value", [60001, '60001'])
def test_validate_recv_window_greater_than_60000(value):
    with pytest.raises(BadParameter, match=f'{value}. Cannot exceed 60000'):
        validate_recv_window(None, None, value)


@pytest.mark.parametrize("value", ['G', 'LL', 'FF', 'BB', 2, None])
def test_validate_locked_free_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: L | F | B'):
        validate_locked_free(None, None, value)


@pytest.mark.parametrize("balances,expected", [
    (None, []),
    ([], [])
])
def test_filter_balances_account_info_return_empty(balances, expected):
    assert filter_balances(balances) == expected


@pytest.mark.parametrize("balances, param, indexes, expected", [
    (get_balances(), 'L', [2], [
        {
            "asset": "BNB",
            "free": "0.00000000",
            "locked": "10.250"
        }
    ]),
    (get_balances(), 'B', [0, 1, 2], get_balances()),
    (get_balances(), 'F', [0, 1], [
        {
            "asset": "BTC",
            "free": "4723846.89208129",
            "locked": "0.00000000"
        },
        {
            "asset": "LTC",
            "free": "4763368.68006011",
            "locked": "0.00000000"
        }
    ])
])
def test_filter_balances_account_info_ok(balances, param, indexes, expected):
    filtered_balances = filter_balances(balances, param)

    assert len(filtered_balances) == len(expected)

    i = 0
    for ex in expected:
        assert balances[indexes[i]] == ex
        assert balances[indexes[i]]['asset'] == ex['asset']
        assert balances[indexes[i]]['free'] == ex['free']
        assert balances[indexes[i]]['locked'] == ex['locked']
        i += 1
