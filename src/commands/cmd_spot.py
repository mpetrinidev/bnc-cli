import click
import requests_async as requests

from src.cli import pass_environment
from src.utils.globals import *
from src.utils.api_time import ApiTime
from src.utils.security import Security
from src.utils.utils import to_query_string_parameters, coro


def validate_recv_window(ctx, param, value):
    if int(value) > 60000:
        raise click.BadParameter(str(value) + '. Cannot exceed 60000')

    return value


def validate_locked_free(ctx, param, value):
    value = str(value).upper()
    if value not in ['L', 'F', 'B']:
        raise click.BadParameter(value + '. Possible values: L | F | B')

    return value


def filter_balances_account_info(balances, locked_free):
    locked_free = locked_free.upper()

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
@click.option("-lf", "--locked_free", default="B", show_default=True, callback=validate_locked_free,
              type=click.types.STRING)
@pass_environment
@coro
async def account_info(ctx, recv_window, locked_free):
    """Get current account information"""
    payload = {'recvWindow': recv_window, 'timestamp': ApiTime.get_timestamp()}
    total_params = to_query_string_parameters(payload)

    payload['signature'] = Security.get_hmac_hash(total_params, Security.get_secret_key())
    headers = Security.get_api_key_header()

    r = await requests.get(API_BINANCE + 'api/v3/account', headers=headers, params=payload)

    if r.status_code != 200:
        return 'Wrong request: status_code: ' + str(r.status_code)

    results = r.json()
    results['balances'] = filter_balances_account_info(results['balances'], locked_free)

    ctx.log('OK')
    return results
