import logging
import os

import click
import json_log_formatter

from bnc.utils.config import read_configuration

formatter = json_log_formatter.JSONFormatter()
filename = os.path.join(os.path.expanduser("~"), read_configuration()["bnc_config_path"], "logs", "log.json")
os.makedirs(os.path.dirname(filename), exist_ok=True)

json_handler = logging.FileHandler(filename=filename)
json_handler.setFormatter(formatter)

logger = logging.getLogger('bnc_file_logger')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)


class ColorFormatter(logging.Formatter):
    colors = {
        'error': dict(fg='red'),
        'exception': dict(fg='red'),
        'critical': dict(fg='red'),
        'debug': dict(fg='cyan'),
        'warning': dict(fg='yellow')
    }

    def format(self, record):
        if not record.exc_info:
            level = record.levelname.lower()
            msg = record.getMessage()
            if level in self.colors:
                prefix = click.style('{}: '.format(level),
                                     **self.colors[level])
                msg = '\n'.join(prefix + x for x in msg.splitlines())
            return msg
        return logging.Formatter.format(self, record)


class ClickHandler(logging.Handler):
    _use_stderr = True

    def emit(self, record):
        try:
            msg = self.format(record)
            level = record.levelname.lower()
            click.echo(msg, err=self._use_stderr)
        except Exception:
            self.handleError(record)


_default_handler = ClickHandler()
_default_handler.formatter = ColorFormatter()

logger_cli = logging.getLogger('bnc_cli_logger')
logger_cli.setLevel(logging.DEBUG)
logger_cli.handlers = [_default_handler]
logger_cli.propagate = False
