import os
import click

from .environment import pass_environment
from .utils.config import write_configuration_file
from .validation.val_cli import validate_output_value

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class BncCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            path = os.path.dirname(__file__)
            folder_name = os.path.basename(path)

            mod = __import__(f"{folder_name}.commands.cmd_{name}", None, None, ["cli"])
        except ImportError:
            return

        return mod.cli


def entry_point():
    try:
        cli()
    except Exception as e:
        msg = [
            click.style(f'[exception]', **dict(fg='red')),
            ' ',
            str(e),
            '\n',
            click.style(f'[info]', **dict(fg='blue')),
            ' ',
            'Submit an issue with --verbose details in https://github.com/mpetrinidev/bnc-cli/issues for help'
        ]

        click.echo(''.join(msg))


@click.command(cls=BncCLI)
@click.option("-v", "--verbose", is_flag=True, help="Show more information about CLI's execution")
@click.option("-o", "--output", default='json', callback=validate_output_value, type=click.types.STRING)
@click.version_option(message="%(prog)s %(version)s")
@pass_environment
def cli(ctx, verbose, output):
    """Binance command line interface to interact with Binance API."""
    write_configuration_file()

    ctx.set_verbose(verbose)
    ctx.set_output(output)
