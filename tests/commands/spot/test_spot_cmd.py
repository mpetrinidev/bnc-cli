from bnc.commands.cmd_spot import cli, new_order
from tests.commands.common_fixtures import *


def test_cli_root_is_ok(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_new_order_root_is_ok(runner):
    result = runner.invoke(new_order)
    assert result.exit_code == 0
