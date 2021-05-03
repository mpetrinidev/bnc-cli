import click

from ..environment import pass_environment

from ..utils.config import remove_credentials
from ..utils.config import write_credentials_file

from ..utils.security import get_api_key
from ..utils.security import get_secret_key


@click.group(short_help="Add or remove Binance CLI credentials (api_key and secret)")
def cli():
    """Add or remove Binance CLI credentials (api_key and secret)"""


@cli.command("add", short_help="Add Binance CLI's credentials (api_key and secret) to start using Binance CLI")
@click.option("-ak", "--api_key", required=True, type=click.types.STRING)
@click.option("-s", "--secret", required=True, type=click.types.STRING)
@pass_environment
def add(ctx, api_key: str, secret: str):
    """Add Binance CLI's credentials (api_key and secret) to start using Binance CLI"""
    write_credentials_file(api_key, secret)
    ctx.log("Binance CLI's credentials added successfully")


@cli.command('remove', short_help="Remove Binance CLI's credentials (api_key and secret)")
@pass_environment
def remove(ctx):
    """Remove Binance CLI's credentials (api_key and secret).

    WARNING: You cannot use Binance CLI again until you add new credentials.
    """
    remove_credentials()

    ctx.log("Binance CLI's credentials removed successfully. \n\nRe-run <bnc credentials add> to start using again "
            "Binance CLI")


@cli.command('show', short_help="Show credentials")
@pass_environment
def show(ctx):
    """Show Binance CLI's credentials"""
    api_key = get_api_key()
    secret = get_secret_key()

    ctx.log(f'BNC_CLI_API_KEY: {api_key}')
    ctx.log(f'BNC_CLI_SECRET_KEY: {secret}')
