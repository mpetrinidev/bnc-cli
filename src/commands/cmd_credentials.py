import click

from src.cli import pass_environment
from src.exceptions import ConfigException
from src.utils.config import write_credentials, remove_credentials, read_credentials


@click.group(short_help="Add or remove Binance CLI credentials (api_key and secret)")
def cli():
    pass


@cli.command("add", short_help="Add Binance CLI's credentials (api_key and secret) to start using Binance CLI")
@click.option("-ak", "--api_key", required=True, type=click.types.STRING)
@click.option("-s", "--secret", required=True, type=click.types.STRING)
@pass_environment
def add(ctx, api_key: str, secret: str):
    """Add Binance CLI's credentials (api_key and secret) to start using Binance CLI"""
    write_credentials(api_key, secret)
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
    try:
        credentials = read_credentials()

        ctx.log(f'BNC_CLI_API_KEY: {credentials["api_key"]}')
        ctx.log(f'BNC_CLI_SECRET_KEY: {credentials["secret"]}')
    except ConfigException as e:
        ctx.log('There was an error trying to read credentials. Enable --verbose for more information')

        ctx.vlog(f'Error: {e.message}')
