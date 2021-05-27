import sys, time
from datetime import datetime
from logging import LogRecord

import click
import pytest

from bnc.logger import BncLoggerColorFormatter
from bnc.logger import BncLoggerFilter
from bnc.logger import BncLoggerHandler

from bnc.logger import logger


@pytest.fixture(scope='session')
def msg():
    return "Logging info message"


@pytest.fixture
def record(msg):
    return LogRecord(name="logger", level=20, pathname=__name__, lineno=1, msg=msg, args={}, exc_info=None)


def test_logger_formatter_info_level_message_ok(msg, record):
    logger_formatter = BncLoggerColorFormatter()

    c_time = time.time()
    record.created = c_time
    record.copy_extra = None
    result = logger_formatter.format(record)

    expected_style = click.style(f'{datetime.fromtimestamp(record.created)} [info] ',
                                 **dict(fg='blue'))

    assert result == f"{expected_style}{msg}"


def test_logger_formatter_exc_info_message_ok(msg, record):
    logger_formatter = BncLoggerColorFormatter()
    try:
        raise Exception('Test Exception')
    except Exception:
        record.exc_info = sys.exc_info()

    value = logger_formatter.formatException(record.exc_info)

    result = logger_formatter.format(record)

    assert result == f"{msg}\n{value}"


def test_logger_filter_verbose_is_true(record):
    logger_filter = BncLoggerFilter(verbose=True)
    assert logger_filter.filter(record) is True


def test_logger_handler_emit_msg(msg, record, capsys):
    logger_handler = BncLoggerHandler()
    logger_handler.emit(record)

    captured = capsys.readouterr()

    assert captured.out == f"{msg}\n"


def test_logger_all_components_with_verbose_enabled(msg, capsys, mocker):
    c_time = time.time()
    mocker.patch('time.time', return_value=c_time)

    bnc_logger = logger
    logger.addFilter(BncLoggerFilter(True))

    bnc_logger.info(msg)

    captured = capsys.readouterr()

    assert captured.out == f'{datetime.fromtimestamp(c_time)} [info] {msg}\n'
