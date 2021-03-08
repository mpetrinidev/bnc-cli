from enum import Enum, unique
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

from src.utils.utils import to_query_string_parameters, generate_output
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


def validate_side(ctx, param, value):
    value = str(value).upper()

    if value not in ['BUY', 'SELL']:
        raise click.BadParameter(value + '. Possible values: BUY | SELL')

    return value


def validate_time_in_force(ctx, param, value):
    if value is None:
        return value

    value = str(value).upper()

    if value not in ['GTC', 'IOC', 'FOK']:
        raise click.BadParameter(value + '. Possible values: GTC | IOC | FOK')

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


@click.group(short_help="Spot Account/Trade operations")
def cli():
    pass


@cli.group("new_order")
def new_order():
    pass


@unique
class Side(Enum):
    BUY = 1
    SELL = 2


@new_order.command("limit", short_help="Send in a new limit order")
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-si", "--side", required=True, callback=validate_side, type=click.types.STRING)
@click.option("-tif", "--time_in_force", required=True, callback=validate_time_in_force, type=click.types.STRING)
@click.option("-q", "--quantity", required=True, type=click.types.FLOAT)
@click.option("-qoq", "--quote_order_qty", type=click.types.FLOAT)
@click.option("-p", "--price", required=True, type=click.types.FLOAT)
@click.option("-ncoid", "--new_client_order_id", type=click.types.STRING)
@click.option("-sp", "--stop_price", type=click.types.FLOAT)
@click.option("-iq", "--iceberg_qty", type=click.types.FLOAT)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
async def limit(symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                stop_price, iceberg_qty, recv_window):

    payload = {'symbol': symbol, 'side': side, 'type': "LIMIT", 'timeInForce': time_in_force, 'quantity': quantity}

    if quote_order_qty is not None:
        payload['quoteOrderQty'] = quote_order_qty

    payload['price'] = price

    if new_client_order_id is not None:
        payload['newClientOrderId'] = new_client_order_id

    if stop_price is not None:
        payload['stopPrice'] = stop_price

    if iceberg_qty is not None:
        payload['icebergQty'] = iceberg_qty

    payload['newOrderRespType'] = "FULL"
    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    total_params = to_query_string_parameters(payload)
    payload['signature'] = get_hmac_hash(total_params, get_secret_key())

    headers = get_api_key_header()

    r = await requests.post(API_BINANCE + 'api/v3/order', headers=headers, params=payload)
    res = handle_response(r=r)

    if not res['successful']:
        return

    generate_output(res['results'])


@cli.command("account_info", short_help="Get current account information")
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@click.option("-lf", "--locked_free", callback=validate_locked_free, type=click.types.STRING)
@coro
async def account_info(recv_window, locked_free):
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


@cli.command("order_status", short_help="Check an order's status")
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-oid", "--order_id", type=click.types.INT)
@click.option("-ocoid", "--orig_client_order_id", type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
@pass_environment
async def order_status(ctx, symbol, order_id, orig_client_order_id, recv_window):
    """
    Check an order's status

    Notes:

        Either --order_id (-oid) or --orig_client_order_id (-ocoid) must be sent.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.
    """
    if order_id is None and orig_client_order_id is None:
        ctx.log('Either --order_id (-oid) or --orig_client_order_id (-ocoid) must be sent.')
        return

    payload = {'symbol': symbol, 'recvWindow': recv_window, 'timestamp': get_timestamp()}
    if order_id is not None:
        payload['orderId'] = order_id

    if orig_client_order_id is not None:
        payload['origClientOrderId'] = orig_client_order_id

    total_params = to_query_string_parameters(payload)
    payload['signature'] = get_hmac_hash(total_params, get_secret_key())
    headers = get_api_key_header()

    r = await requests.get(API_BINANCE + 'api/v3/order', headers=headers, params=payload)
    res = handle_response(r=r)

    if not res['successful']:
        return

    generate_output(res['results'])
