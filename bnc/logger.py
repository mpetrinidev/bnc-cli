import logging
from datetime import datetime

import click

from bnc.utils.utils import to_log_str


class BncLoggerColorFormatter(logging.Formatter):
    colors = {
        'error': dict(fg='red'),
        'info': dict(fg='blue'),
        'debug': dict(fg='white'),
        'warning': dict(fg='yellow')
    }

    def format(self, record: logging.LogRecord) -> str:
        if not record.exc_info:
            final_msg = []
            level = record.levelname.lower()
            msg = record.getMessage()
            extra = record.copy_extra

            if level in self.colors:
                final_msg.append(click.style(f'{datetime.fromtimestamp(record.created)} [{level}] ',
                                             **self.colors[level]))
                for line in msg.splitlines():
                    final_msg.append(line)

            if extra is not None:
                final_msg.append(' ')
                final_msg.append(to_log_str(extra))

            return ''.join(final_msg)

        return logging.Formatter.format(self, record)


class BncLoggerFilter(logging.Filter):
    def __init__(self, verbose):
        super().__init__()
        self.verbose = verbose

    def filter(self, record: logging.LogRecord) -> bool:
        return self.verbose


class BncLoggerHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            click.echo(msg)
        except Exception:
            self.handleError(record)


def make_record_with_extra(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
    record = original_makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
    record.copy_extra = extra
    return record


original_makeRecord = logging.Logger.makeRecord
logging.Logger.makeRecord = make_record_with_extra

_default_handler = BncLoggerHandler()
_default_handler.formatter = BncLoggerColorFormatter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.handlers = [_default_handler]
