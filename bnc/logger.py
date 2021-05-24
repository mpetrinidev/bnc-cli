import logging

import click


class BncLoggerColorFormatter(logging.Formatter):
    colors = {
        'ERRROR': dict(fg='red'),
        'EXCEPTION': dict(fg='red'),
        'CRITICAL': dict(fg='red'),
        'DEBUG': dict(fg='cyan'),
        'WARNING': dict(fg='yellow')
    }

    def format(self, record: logging.LogRecord) -> str:
        if not record.exc_info:
            level = record.levelname
            msg = record.getMessage()
            if level in self.colors:
                prefix = click.style('[{}] '.format(level),
                                     **self.colors[level])
                msg = '\n'.join(prefix + x for x in msg.splitlines())
            return msg
        return logging.Formatter.format(self, record)


class BncLoggerFilter(logging.Filter):
    def __init__(self, verbose):
        super().__init__()
        self.verbose = verbose

    def filter(self, record: logging.LogRecord) -> bool:
        return self.verbose


class BncLoggerHandler(logging.Handler):
    _use_stderr = True

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            click.echo(msg, err=self._use_stderr)
        except Exception:
            self.handleError(record)


_default_handler = BncLoggerHandler()
_default_handler.formatter = BncLoggerColorFormatter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = [_default_handler]
