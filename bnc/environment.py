import uuid

import click

from .logger import logger, logger_cli


class Environment:
    def __init__(self):
        self.log_id = str(uuid.uuid4())
        self.logger = logger
        self.logger_cli = logger_cli
        self.verbose = False
        self.output = 'json'

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args

        click.echo(click.style(msg))

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def json_log(self, msg, extra):
        extra['log_id'] = self.log_id
        self.logger.info(msg, extra=extra)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
