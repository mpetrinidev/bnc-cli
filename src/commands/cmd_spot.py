import click

from src.cli import pass_environment


def validate_recv_window(ctx, param, value):
    if int(value) > 60000:
        raise click.BadParameter(str(value) + '. Cannot exceed 60000')

    return value


def validate_locked_free(ctx, param, value):
    value = str(value).upper()
    if value not in ['L', 'F', 'B']:
        raise click.BadParameter(value + '. Possible values: L | F | B')

    return value


@click.group(short_help="Functionalities related to spot account/trade")
def cli():
    pass


@cli.command("account_info", short_help="Get current account information")
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@click.option("-lf", "--locked_free", default="B", show_default=True, callback=validate_locked_free,
              type=click.types.STRING)
@pass_environment
def account_info(ctx, recv_window, locked_free):
    """Get current account information"""
    ctx.log('OK')
