import click

from .logger import logger, BncLoggerFilter


class Environment:
    def __init__(self):
        self.verbose = False
        self.logger = None
        self.output = 'json'

    def set_verbose(self, verbose):
        self.verbose = verbose

        logger.addFilter(BncLoggerFilter(verbose))
        self.logger = logger

    def set_output(self, output):
        self.output = output

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args

        click.echo(click.style(msg))


pass_environment = click.make_pass_decorator(Environment, ensure=True)
