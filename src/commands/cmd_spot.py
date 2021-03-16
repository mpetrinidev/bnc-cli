import click

from src.builder import Builder, AccountInfoBuilder
from src.cli import pass_environment
from src.decorators import coro

from src.validation.val_spot import validate_side
from src.validation.val_spot import validate_recv_window
from src.validation.val_spot import validate_locked_free
from src.validation.val_spot import validate_time_in_force

from src.utils.api_time import get_timestamp


@click.group(short_help="Spot Account/Trade operations")
def cli():
    pass


@cli.group("new_order", short_help="Send in a new limit, "
                                   "market, stop_loss, stop_loss_limit, "
                                   "take_profit, take_profit_limit "
                                   "or limit_maker order")
def new_order():
    pass


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
    """Send in a new limit order"""
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

    builder = Builder(endpoint='api/v3/order', payload=payload, method='POST') \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("account_info", short_help="Get current account information")
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@click.option("-lf", "--locked_free", callback=validate_locked_free, type=click.types.STRING)
@coro
async def account_info(recv_window, locked_free):
    """Get current account information"""
    payload = {'recvWindow': recv_window, 'timestamp': get_timestamp()}

    builder = AccountInfoBuilder(endpoint='api/v3/account', payload=payload) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().filter(locked_free=locked_free).generate_output()


@cli.command("open_orders", short_help="Get all open orders on a symbol. Careful when accessing this with no symbol.")
@click.option("-sy", "--symbol", type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
async def open_orders(symbol, recv_window):
    """
    Get all open orders on a symbol. Careful when accessing this with no symbol.

    Weight: 1 for a single symbol; 40 when the symbol parameter is omitted
    """
    payload = {'recvWindow': recv_window, 'timestamp': get_timestamp()}
    if symbol is not None:
        payload['symbol'] = symbol

    builder = Builder(endpoint='api/v3/openOrders', payload=payload).set_security()
    await builder.send_http_req()

    builder.handle_response().generate_output()


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

    builder = Builder(endpoint='api/v3/order', payload=payload) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()
