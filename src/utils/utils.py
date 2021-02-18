import asyncio
from functools import wraps


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def to_query_string_parameters(values: {}) -> str:
    if not values:
        raise ValueError('values cannot be empty')

    return '&'.join(key + '=' + str(val) for key, val in values.items())
