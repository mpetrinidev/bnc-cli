import click

from src.builder import AccountInfoBuilder, LimitOrderBuilder, MarketOrderBuilder, StopLossBuilder, \
    StopLossLimitBuilder, TakeProfitBuilder, TakeProfitLimitBuilder, LimitMakerBuilder, CancelOrderBuilder, \
    OpenOrdersBuilder, OrderStatusBuilder, Builder, AllOrderBuilder
from src.cli import pass_environment
from src.decorators import coro, new_order_options
from src.utils.api_time import get_timestamp
from src.validation.val_spot import validate_locked_free
from src.validation.val_spot import validate_recv_window


@click.group(short_help="Spot Account/Trade operations")
def cli():
    """Spot Account/Trade operations"""
    pass


@cli.group("new_order", short_help="Send in a new limit, "
                                   "market, stop_loss, stop_loss_limit, "
                                   "take_profit, take_profit_limit "
                                   "or limit_maker order")
def new_order():
    """
    Send in a new limit, market, stop_loss, stop_loss_limit, take_profit, take_profit_limit or limit_maker order
    """
    pass


@new_order.command("limit", short_help="Send in a new limit order")
@new_order_options([{'name': '-tif', 'attrs': {'required': True}},
                    {'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}}])
@coro
async def limit(symbol, side, time_in_force, quantity, quote_order_qty, price, new_client_order_id,
                stop_price, iceberg_qty, recv_window, new_order_resp_type):
    """Send in a new limit order"""
    payload = {
        'symbol': symbol,
        'side': side,
        'type': "LIMIT",
        'timeInForce': time_in_force,
        'price': price,
        'quantity': quantity,
        'newOrderRespType': new_order_resp_type,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = LimitOrderBuilder(endpoint='api/v3/order', payload=payload, method='POST') \
        .add_optional_params_to_payload(quote_order_qty=quote_order_qty,
                                        new_client_order_id=new_client_order_id,
                                        stop_price=stop_price,
                                        iceberg_qty=iceberg_qty) \
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

    payload = {
        'symbol': symbol,
        'side': side,
        'type': "MARKET",
        'newOrderRespType': new_order_resp_type,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = MarketOrderBuilder(endpoint='api/v3/order', payload=payload, method='POST') \
        .add_optional_params_to_payload(quantity=quantity, time_in_force=time_in_force,
                                        quote_order_qty=quote_order_qty, price=price,
                                        new_client_order_id=new_client_order_id,
                                        stop_price=stop_price, iceberg_qty=iceberg_qty) \
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
    payload = {
        'symbol': symbol,
        'side': side,
        'type': "STOP_LOSS",
        'quantity': quantity,
        'stopPrice': stop_price,
        'newOrderRespType': new_order_resp_type,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = StopLossBuilder(endpoint='api/v3/order', payload=payload, method='POST') \
        .add_optional_params_to_payload(time_in_force=time_in_force,
                                        quote_order_qty=quote_order_qty,
                                        price=price,
                                        new_client_order_id=new_client_order_id,
                                        iceberg_qty=iceberg_qty) \
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
    payload = {
        'symbol': symbol,
        'side': side,
        'type': "STOP_LOSS_LIMIT",
        'timeInForce': time_in_force,
        'quantity': quantity,
        'price': price,
        'stopPrice': stop_price,
        'newOrderRespType': new_order_resp_type,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = StopLossLimitBuilder(endpoint='api/v3/order', payload=payload, method='POST') \
        .add_optional_params_to_payload(quote_order_qty=quote_order_qty,
                                        new_client_order_id=new_client_order_id,
                                        iceberg_qty=iceberg_qty) \
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
    payload = {
        'symbol': symbol,
        'side': side,
        'type': "TAKE_PROFIT",
        'quantity': quantity,
        'stopPrice': stop_price,
        'newOrderRespType': new_order_resp_type,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = TakeProfitBuilder(endpoint='api/v3/order', payload=payload, method='POST') \
        .add_optional_params_to_payload(time_in_force=time_in_force,
                                        quote_order_qty=quote_order_qty,
                                        price=price,
                                        new_client_order_id=new_client_order_id,
                                        iceberg_qty=iceberg_qty) \
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
    payload = {
        'symbol': symbol,
        'side': side,
        'type': "TAKE_PROFIT_LIMIT",
        'timeInForce': time_in_force,
        'quantity': quantity,
        'price': price,
        'stopPrice': stop_price,
        'newOrderRespType': new_order_resp_type,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = TakeProfitLimitBuilder(endpoint='api/v3/order', payload=payload, method='POST') \
        .add_optional_params_to_payload(quote_order_qty=quote_order_qty,
                                        new_client_order_id=new_client_order_id,
                                        iceberg_qty=iceberg_qty) \
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
    payload = {
        'symbol': symbol,
        'side': side,
        'type': "LIMIT_MAKER",
        'quantity': quantity,
        'price': price,
        'newOrderRespType': new_order_resp_type,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = LimitMakerBuilder(endpoint='api/v3/order', payload=payload, method='POST') \
        .add_optional_params_to_payload(time_in_force=time_in_force,
                                        quote_order_qty=quote_order_qty,
                                        stop_price=stop_price,
                                        new_client_order_id=new_client_order_id,
                                        iceberg_qty=iceberg_qty) \
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

    payload = {
        'symbol': symbol,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = CancelOrderBuilder(endpoint='api/v3/order', payload=payload, method='DELETE') \
        .add_optional_params_to_payload(order_id=order_id,
                                        orig_client_order_id=orig_client_order_id,
                                        new_client_order_id=new_client_order_id) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("cancel_all_orders", short_help='Cancels all active orders on a symbol. '
                                             'This includes OCO orders.')
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
async def cancel_all_orders(symbol, recv_window):
    """
    Cancels all active orders on a symbol.
    This includes OCO orders.
    """

    payload = {
        'symbol': symbol,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = Builder(endpoint='api/v3/openOrders', payload=payload, method='DELETE').set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("account_info", short_help="Get current account information")
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@click.option("-lf", "--locked_free", callback=validate_locked_free, type=click.types.STRING)
@coro
async def account_info(recv_window, locked_free):
    """Get current account information"""
    payload = {
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = AccountInfoBuilder(endpoint='api/v3/account', payload=payload) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().filter(locked_free=locked_free).generate_output()


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

    payload = {
        'symbol': symbol,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = OrderStatusBuilder(endpoint='api/v3/order', payload=payload) \
        .add_optional_params_to_payload(order_id=order_id,
                                        orig_client_order_id=orig_client_order_id) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("open_orders", short_help="Get all open orders on a symbol. Careful when accessing this with no symbol.")
@click.option("-sy", "--symbol", type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
async def open_orders(symbol, recv_window):
    """
    Get all open orders on a symbol. Careful when accessing this with no symbol.

    Weight:
        1 for a single symbol.
        40 when the symbol parameter is omitted.
    """
    payload = {
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = OpenOrdersBuilder(endpoint='api/v3/openOrders', payload=payload) \
        .add_optional_params_to_payload(symbol=symbol) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("all_orders", short_help="Get all account orders; active, canceled, or filled.")
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-oid", "--order_id", type=click.types.INT)
@click.option("-st", "--start_time", type=click.types.INT)
@click.option("-et", "--end_time", type=click.types.INT)
@click.option("-l", "--limit", default=500, show_default=True, type=click.types.IntRange(1, 1000))
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@click.option("-q", "--query", type=click.types.STRING)
@coro
async def all_orders(symbol, order_id, start_time, end_time, limit, recv_window, query):
    """
    Get all account orders; active, canceled, or filled.

    Weight: 5 with symbol.

    NOTES:

        If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.
    """
    payload = {
        'symbol': symbol,
        'limit': limit,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = AllOrderBuilder(endpoint='api/v3/allOrders', payload=payload) \
        .add_optional_params_to_payload(order_id=order_id,
                                        start_time=start_time,
                                        end_time=end_time) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().filter(query).generate_output()
