from typing import List

import click
import requests_async as requests

from src.cli import pass_environment
from src.utils.globals import API_BINANCE

from src.utils.api_time import get_timestamp
from src.utils.http import handle_response
from src.utils.security import get_hmac_hash
from src.utils.security import get_secret_key
from src.utils.security import get_api_key_header

from src.utils.utils import to_query_string_parameters, json_to_str, json_to_table, generate_output
from src.utils.utils import coro


def validate_recv_window(ctx, param, value):
    if value is None:
        raise click.BadParameter('recv_window cannot be null')

    if int(value) > 60000:
        raise click.BadParameter(str(value) + '. Cannot exceed 60000')

    return value


def validate_locked_free(ctx, param, value):
    if value is None:
        return

    value = str(value).upper()
    if value not in ['L', 'F', 'B']:
        raise click.BadParameter(value + '. Possible values: A | L | F | B')

    return value


def filter_balances(balances: List, locked_free: str = 'A'):
    locked_free = locked_free.upper()

    if balances is None:
        return []

    if len(balances) == 0:
        return balances

    if locked_free == 'B':
        balances = [x for x in balances if float(x['free']) > 0.0 or float(x['locked']) > 0.0]
    elif locked_free == 'F':
        balances = [x for x in balances if float(x['free']) > 0.0]
    elif locked_free == 'L':
        balances = [x for x in balances if float(x['locked']) > 0.0]

    return balances


@click.group(short_help="Functionalities related to spot account/trade")
def cli():
    pass


@cli.command("account_info", short_help="Get current account information")
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@click.option("-lf", "--locked_free", callback=validate_locked_free, type=click.types.STRING)
@pass_environment
@coro
async def account_info(ctx, recv_window, locked_free):
    """Get current account information"""
    payload = {'recvWindow': recv_window, 'timestamp': get_timestamp()}
    total_params = to_query_string_parameters(payload)

    payload['signature'] = get_hmac_hash(total_params, get_secret_key())
    headers = get_api_key_header()

    r = await requests.get(API_BINANCE + 'api/v3/account', headers=headers, params=payload)
    res = handle_response(r=r)

    if not res['successful']:
        return

    if locked_free is not None:
        res['results']['balances'] = filter_balances(res['results']['balances'], locked_free)

    generate_output(res['results'])
