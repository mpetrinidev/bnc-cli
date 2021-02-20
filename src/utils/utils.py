import asyncio
from functools import wraps

import click


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def get_current_context():
    return click.get_current_context()


def to_query_string_parameters(values: {}) -> str:
    if not values:
        raise ValueError('values cannot be empty')

    return '&'.join(key + '=' + str(val) for key, val in values.items())
