import asyncio
import json

from pandas import json_normalize
from functools import wraps

import click


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def json_to_str(value, indent: int = 2):
    return json.dumps(value, indent=indent)


def json_to_table(value):
    return json_normalize(value, "balances", ['asset', 'free', 'locked'])


def get_current_context():
    return click.get_current_context()


def to_query_string_parameters(values: {}) -> str:
    if not values:
        raise ValueError('values cannot be empty')

    return '&'.join(key + '=' + str(val) for key, val in values.items())
