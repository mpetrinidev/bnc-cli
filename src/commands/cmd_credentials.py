import click

from src.cli import pass_environment
from src.utils.security import Security
from src.utils.utils import write_credentials_config_file


@click.group(short_help="Add or remove Binance CLI credentials (api_key and secret)")
def cli():
    pass


@cli.command("add", short_help="Add Binance CLI's credentials (api_key and secret) to start using Binance CLI")
@click.option("-ak", "--api_key", required=True, type=click.types.STRING)
@click.option("-s", "--secret", required=True, type=click.types.STRING)
@pass_environment
def add(ctx, api_key: str, secret: str):
    """Add Binance CLI's credentials (api_key and secret) to start using Binance CLI"""
    write_credentials_config_file(api_key, secret)

    Security.set_secret_key(secret)
    Security.set_api_key(api_key)

    ctx.log("Binance CLI's credentials added successfully")


@cli.command('remove', short_help="Remove Binance CLI's credentials (api_key and secret)")
@pass_environment
def remove(ctx):
    """Remove Binance CLI's credentials (api_key and secret).

    WARNING: You cannot use Binance CLI again until you add new credentials.
    """
    Security.del_secret_key()
    Security.del_api_key()

    ctx.log("Binance CLI's credentials removed successfully. \n\nRe-run <bnc credentials add> to start using again "
            "Binance CLI")
