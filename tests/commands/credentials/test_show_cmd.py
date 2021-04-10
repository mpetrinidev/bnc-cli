from tests.commands.common_fixtures import *
from src.commands.cmd_credentials import show
from src.utils.config import write_credentials
from src.utils.config import remove_credentials


def test_credentials_show_successfully(runner):
    write_credentials("API_KEY_VALUE", "SECRET_KEY_VALUE")

    result = runner.invoke(show)

    assert result.exit_code == 0
    assert result.output == "BNC_CLI_API_KEY: API_KEY_VALUE\nBNC_CLI_SECRET_KEY: SECRET_KEY_VALUE\n"

    remove_credentials()
