from src.cli import pass_environment

import click

from src.utils.security import Security


@click.group(short_help="Add or remove Binance CLI credentials (api_key and secret)")
def cli():
    pass


@cli.command("add", short_help="Add Binance CLI's credentials (api_key and secret) to start using Binance CLI")
@click.argument("api_key", required=True, type=str)
@click.argument("secret", required=True, type=str)
@pass_environment
def add(ctx, api_key: str, secret: str):
    """Add Binance CLI's credentials (api_key and secret) to start using Binance CLI"""
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
