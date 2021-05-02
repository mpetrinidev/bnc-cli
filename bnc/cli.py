import os
import sys
import uuid

import click

from .logger import logger
from .utils.config import write_configuration_file
from .validation.val_cli import validate_output_value


class Environment:
    def __init__(self):
        self.log_id = str(uuid.uuid4())
        self.logger = logger
        self.verbose = False
        self.output = 'json'

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def json_log(self, msg, extra):
        extra['log_id'] = self.log_id
        self.logger.info(msg, extra=extra)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
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


@click.command(cls=BncCLI)
@click.option("-v", "--verbose", is_flag=True, help="Show more information about CLI's execution")
@click.option("-o", "--output", default='json', callback=validate_output_value, type=click.types.STRING)
@click.version_option(message="%(prog)s %(version)s")
@pass_environment
def cli(ctx, verbose, output):
    """Binance command line interface to interact with Binance API."""
    write_configuration_file()

    ctx.verbose = verbose
    ctx.output = output
