import asyncio
from functools import wraps

import click

from src.options import get_new_order_default_options


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def new_order_options(overrides: [] = None):
    def wrapper(func):
        for config_option in reversed(get_new_order_default_options()):
            if overrides is not None:
                for name in reversed(config_option['params']):
                    lst = list(filter(lambda d: d['name'] == name, overrides))
                    if not lst:
                        continue

                    config_option['attrs'].update(lst[0]['attrs'])

            option = click.option(*config_option['params'], **config_option['attrs'])
            func = option(func)

        return func

    return wrapper
