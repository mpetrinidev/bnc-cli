import asyncio
from functools import wraps

import click

from .options import get_new_order_default_options
from .utils.security import get_api_key, get_secret_key


def check_credentials(f):
    def inner():
        _ = get_api_key()
        _ = get_secret_key()
        f()

    return inner


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def new_order_options(overrides: [] = None):
    def wrapper(func):
        options = get_new_order_default_options()
        for i in reversed(range(len(options))):
            def_opt = options[i]
            keys = list(def_opt.keys())

            if overrides is not None:
                ov = next((i for i in overrides if i['name'] == keys[0] or i['name'] == keys[1]), None)
                if ov is not None:
                    if 'exclude' in ov and ov['exclude'] is True:
                        continue

                    def_opt['attrs'].update(ov['attrs'])

            option = click.option(*[keys[0], keys[1]], **def_opt['attrs'])
            func = option(func)

        return func

    return wrapper
