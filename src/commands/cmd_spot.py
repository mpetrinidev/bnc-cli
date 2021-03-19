import click

from src.builder import Builder, AccountInfoBuilder
from src.cli import pass_environment
from src.decorators import coro

from src.validation.val_spot import validate_side, validate_new_order_resp_type
from src.validation.val_spot import validate_recv_window
from src.validation.val_spot import validate_locked_free
from src.validation.val_spot import validate_time_in_force

from src.utils.api_time import get_timestamp


def get_new_order_config_options():
    return [
        {'params': ['-sy', '--symbol'], 'attrs': {'required': True, 'type': click.types.STRING}},
        {'params': ['-si', '--side'], 'attrs': {'required': True, 'callback': validate_side,
                                                'type': click.types.STRING}},
        {'params': ['-tif', '--time_in_force'], 'attrs': {'callback': validate_time_in_force,
                                                          'type': click.types.STRING}},
        {'params': ['-q', '--quantity'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-qoq', '--quote_order_qty'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-p', '--price'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-ncoid', '--new_client_order_id'], 'attrs': {'type': click.types.STRING}},
        {'params': ['-sp', '--stop_price'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-iq', '--iceberg_qty'], 'attrs': {'type': click.types.FLOAT}},
        {'params': ['-rw', '--recv_window'], 'attrs': {'default': 5000, 'show_default': True,
                                                       'callback': validate_recv_window,
                                                       'type': click.types.INT}},
        {'params': ['-nort', '--new_order_resp_type'], 'attrs': {'default': "FULL", 'show_default': True,
                                                                 'callback': validate_new_order_resp_type,
                                                                 'type': click.types.STRING}},
    ]


def new_order_options(overrides: [] = None):
    def wrapper(func):
        for config_option in reversed(get_new_order_config_options()):
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
@new_order_options([{'name': '-tif', 'attrs': {'required': True}},
                    {'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}}])
@coro
async def limit(symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                stop_price, iceberg_qty, recv_window, new_order_resp_type):
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

    payload['newOrderRespType'] = new_order_resp_type
    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    builder = Builder(endpoint='api/v3/order', payload=payload, method='POST') \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("market", short_help="Send in a new market order")
@new_order_options()
@pass_environment
@coro
async def market(ctx, symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                 stop_price, iceberg_qty, recv_window, new_order_resp_type):
    """Send in a new market order"""
    if quantity is None and quote_order_qty is None:
        ctx.log('Either --quantity (-q) or --quote_order_qty (-qoq) must be sent.')
        return

    payload = {'symbol': symbol, 'side': side, 'type': "MARKET"}

    if quantity is not None:
        payload['quantity'] = quantity

    if time_in_force is not None:
        payload['timeInForce'] = time_in_force

    if quote_order_qty is not None:
        payload['quoteOrderQty'] = quote_order_qty

    if price is not None:
        payload['price'] = price

    if new_client_order_id is not None:
        payload['newClientOrderId'] = new_client_order_id

    if stop_price is not None:
        payload['stopPrice'] = stop_price

    if iceberg_qty is not None:
        payload['icebergQty'] = iceberg_qty

    payload['newOrderRespType'] = new_order_resp_type
    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    builder = Builder(endpoint='api/v3/order', payload=payload, method='POST') \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("stop_loss", short_help="Send in a new stop_loss order")
@new_order_options([{'name': '-q', 'attrs': {'required': True}},
                    {'name': '-sp', 'attrs': {'required': True}},
                    {'name': '-nort', 'attrs': {'default': "ACK"}}])
@coro
async def stop_loss(symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                    stop_price, iceberg_qty, recv_window, new_order_resp_type):
    """Send in a new stop_loss order"""
    payload = {'symbol': symbol, 'side': side, 'type': "STOP_LOSS", 'quantity': quantity, 'stopPrice': stop_price}

    if time_in_force is not None:
        payload['timeInForce'] = time_in_force

    if quote_order_qty is not None:
        payload['quoteOrderQty'] = quote_order_qty

    if price is not None:
        payload['price'] = price

    if new_client_order_id is not None:
        payload['newClientOrderId'] = new_client_order_id

    if iceberg_qty is not None:
        payload['icebergQty'] = iceberg_qty

    payload['newOrderRespType'] = new_order_resp_type
    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    builder = Builder(endpoint='api/v3/order', payload=payload, method='POST') \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("stop_loss_limit", short_help="Send in a new stop_loss_limit order")
@new_order_options([{'name': '-tif', 'attrs': {'required': True}},
                    {'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}},
                    {'name': '-sp', 'attrs': {'required': True}},
                    {'name': '-nort', 'attrs': {'default': "ACK"}}])
@coro
async def stop_loss_limit(symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                          stop_price, iceberg_qty, recv_window, new_order_resp_type):
    """Send in a new stop_loss_limit order"""
    payload = {'symbol': symbol, 'side': side, 'type': "STOP_LOSS_LIMIT", 'timeInForce': time_in_force,
               'quantity': quantity, 'price': price, 'stopPrice': stop_price}

    if quote_order_qty is not None:
        payload['quoteOrderQty'] = quote_order_qty

    if price is not None:
        payload['price'] = price

    if new_client_order_id is not None:
        payload['newClientOrderId'] = new_client_order_id

    if iceberg_qty is not None:
        payload['icebergQty'] = iceberg_qty

    payload['newOrderRespType'] = new_order_resp_type
    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    builder = Builder(endpoint='api/v3/order', payload=payload, method='POST') \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("take_profit", short_help="Send in a new take_profit order")
@new_order_options([{'name': '-q', 'attrs': {'required': True}},
                    {'name': '-sp', 'attrs': {'required': True}},
                    {'name': '-nort', 'attrs': {'default': "ACK"}}])
@coro
async def take_profit(symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                      stop_price, iceberg_qty, recv_window, new_order_resp_type):
    """Send in a new take_profit order"""
    payload = {'symbol': symbol, 'side': side, 'type': "TAKE_PROFIT", 'quantity': quantity, 'stopPrice': stop_price}

    if time_in_force is not None:
        payload['timeInForce'] = time_in_force

    if quote_order_qty is not None:
        payload['quoteOrderQty'] = quote_order_qty

    if price is not None:
        payload['price'] = price

    if new_client_order_id is not None:
        payload['newClientOrderId'] = new_client_order_id

    if iceberg_qty is not None:
        payload['icebergQty'] = iceberg_qty

    payload['newOrderRespType'] = new_order_resp_type
    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    builder = Builder(endpoint='api/v3/order', payload=payload, method='POST') \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("take_profit_limit", short_help="Send in a new take_profit_limit order")
@new_order_options([{'name': '-tif', 'attrs': {'required': True}},
                    {'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}},
                    {'name': '-sp', 'attrs': {'required': True}},
                    {'name': '-nort', 'attrs': {'default': "ACK"}}])
@coro
async def take_profit_limit(symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                            stop_price, iceberg_qty, recv_window, new_order_resp_type):
    """Send in a new take_profit_limit order"""
    payload = {'symbol': symbol, 'side': side, 'type': "TAKE_PROFIT_LIMIT", 'timeInForce': time_in_force,
               'quantity': quantity, 'price': price, 'stopPrice': stop_price}

    if quote_order_qty is not None:
        payload['quoteOrderQty'] = quote_order_qty

    if price is not None:
        payload['price'] = price

    if new_client_order_id is not None:
        payload['newClientOrderId'] = new_client_order_id

    if iceberg_qty is not None:
        payload['icebergQty'] = iceberg_qty

    payload['newOrderRespType'] = new_order_resp_type
    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    builder = Builder(endpoint='api/v3/order', payload=payload, method='POST') \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("limit_maker", short_help="Send in a new limit_maker order")
@new_order_options([{'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}},
                    {'name': '-nort', 'attrs': {'default': "ACK"}}])
@coro
async def limit_maker(symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                      stop_price, iceberg_qty, recv_window, new_order_resp_type):
    """Send in a new limit_maker order"""
    payload = {'symbol': symbol, 'side': side, 'type': "LIMIT_MAKER", 'quantity': quantity, 'price': price}

    if time_in_force is not None:
        payload['timeInForce'] = time_in_force

    if quote_order_qty is not None:
        payload['quoteOrderQty'] = quote_order_qty

    if stop_price is not None:
        payload['stopPrice'] = stop_price

    if new_client_order_id is not None:
        payload['newClientOrderId'] = new_client_order_id

    if iceberg_qty is not None:
        payload['icebergQty'] = iceberg_qty

    payload['newOrderRespType'] = new_order_resp_type
    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    builder = Builder(endpoint='api/v3/order', payload=payload, method='POST') \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("cancel_order", short_help='Cancel an active order')
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-oid", "--order_id", type=click.types.INT)
@click.option("-ocoid", "--orig_client_order_id", type=click.types.STRING)
@click.option("-ncoid", "--new_client_order_id", type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@pass_environment
@coro
async def cancel_order(ctx, symbol, order_id, orig_client_order_id, new_client_order_id, recv_window):
    """
    Cancel an active order

    Either orderId or origClientOrderId must be sent.
    """
    if order_id is None and orig_client_order_id is None:
        ctx.log('Either --order_id (-oid) or --orig_client_order_id (-ocoid) must be sent.')
        return

    payload = {'symbol': symbol}

    if order_id is not None:
        payload['orderId'] = order_id

    if orig_client_order_id is not None:
        payload['origClientOrderId'] = orig_client_order_id

    if new_client_order_id is not None:
        payload['newClientOrderId'] = new_client_order_id

    payload['recvWindow'] = recv_window
    payload['timestamp'] = get_timestamp()

    builder = Builder(endpoint='api/v3/order', payload=payload, method='DELETE').set_security()

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
