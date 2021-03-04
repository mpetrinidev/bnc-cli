import os
import sys

import click

CONTEXT_SETTINGS = dict(auto_envvar_prefix="BNC")


def validate_output_value(ctx, param, value):
    value = str(value).lower()
    if value not in ['json', 'table', 'yaml']:
        raise click.BadParameter(value + '. Possible values: json | table | yaml')

    return value


class Environment:
    def __init__(self):
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
            mod = __import__(f"src.commands.cmd_{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=BncCLI, context_settings=CONTEXT_SETTINGS)
@click.option("-v", "--verbose", is_flag=True, help="Show more information about CLI's execution")
@click.option("-o", "--output", default='json', callback=validate_output_value, type=click.types.STRING)
@click.version_option(message="Bnc %(version)s")
@pass_environment
def cli(ctx, verbose, output):
    """Binance command line interface to interact with Binance API."""
    ctx.verbose = verbose
    ctx.output = output
