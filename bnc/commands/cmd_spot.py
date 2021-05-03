import click

from ..builder import LimitOrderBuilder
from ..builder import MarketOrderBuilder
from ..builder import StopLossLimitBuilder
from ..builder import TakeProfitLimitBuilder
from ..builder import LimitMakerBuilder
from ..builder import CancelOrderBuilder
from ..builder import OpenOrdersBuilder
from ..builder import OrderStatusBuilder
from ..builder import Builder
from ..builder import AllOrderBuilder
from ..builder import MyTradesBuilder
from ..builder import NewOcoOrderBuilder
from ..builder import CancelOcoOrderBuilder
from ..builder import OcoOrderBuilder
from ..builder import AllOcoOrderBuilder

from ..environment import pass_environment

from ..decorators import coro
from ..decorators import new_order_options
from ..decorators import check_credentials

from ..utils.api_time import get_timestamp

from ..validation.val_spot import validate_recv_window
from ..validation.val_spot import validate_side
from ..validation.val_spot import validate_time_in_force
from ..validation.val_spot import validate_new_order_resp_type


@click.group(short_help="Spot Account/Trade operations")
@check_credentials
def cli():
    """Spot Account/Trade operations"""


@cli.group("new_order", short_help="Send in a new limit, "
                                   "market, stop_loss, stop_loss_limit, "
                                   "take_profit, take_profit_limit "
                                   "or limit_maker order")
def new_order():
    """
    Send in a new limit, market, stop_loss, stop_loss_limit, take_profit, take_profit_limit or limit_maker order
    """


@new_order.command("limit", short_help="Send in a new limit order")
@new_order_options([{'name': '-tif', 'attrs': {'required': True}},
                    {'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}},
                    {'name': '-qoq', 'exclude': True},
                    {'name': '-sp', 'exclude': True}])
@coro
async def limit(symbol, side, time_in_force, quantity, price, new_client_order_id,
                iceberg_qty, recv_window, new_order_resp_type):
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
        .add_optional_params_to_payload(new_client_order_id=new_client_order_id,
                                        iceberg_qty=iceberg_qty) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("market", short_help="Send in a new market order")
@new_order_options([{'name': '-tif', 'exclude': True},
                    {'name': '-p', 'exclude': True},
                    {'name': '-sp', 'exclude': True},
                    {'name': '-iq', 'exclude': True}])
@pass_environment
@coro
async def market(ctx, symbol, side, quantity, quote_order_qty, new_client_order_id,
                 recv_window, new_order_resp_type):
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
        .add_optional_params_to_payload(quantity=quantity,
                                        quote_order_qty=quote_order_qty,
                                        new_client_order_id=new_client_order_id) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("stop_loss_limit", short_help="Send in a new stop_loss_limit order")
@new_order_options([{'name': '-tif', 'attrs': {'required': True}},
                    {'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}},
                    {'name': '-sp', 'attrs': {'required': True}},
                    {'name': '-nort', 'attrs': {'default': "ACK"}},
                    {'name': '-qoq', 'exclude': True}])
@coro
async def stop_loss_limit(symbol, side, time_in_force, quantity, price, new_client_order_id,
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
        .add_optional_params_to_payload(new_client_order_id=new_client_order_id,
                                        iceberg_qty=iceberg_qty) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("take_profit_limit", short_help="Send in a new take_profit_limit order")
@new_order_options([{'name': '-tif', 'attrs': {'required': True}},
                    {'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}},
                    {'name': '-sp', 'attrs': {'required': True}},
                    {'name': '-nort', 'attrs': {'default': "ACK"}},
                    {'name': '-qoq', 'exclude': True}])
@coro
async def take_profit_limit(symbol, side, time_in_force, quantity, price, new_client_order_id,
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
        .add_optional_params_to_payload(new_client_order_id=new_client_order_id,
                                        iceberg_qty=iceberg_qty) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@new_order.command("limit_maker", short_help="Send in a new limit_maker order")
@new_order_options([{'name': '-q', 'attrs': {'required': True}},
                    {'name': '-p', 'attrs': {'required': True}},
                    {'name': '-tif', 'exclude': True},
                    {'name': '-qoq', 'exclude': True},
                    {'name': '-sp', 'exclude': True},
                    {'name': '-nort', 'attrs': {'default': "ACK"}}])
@coro
async def limit_maker(symbol, side, quantity, price, new_client_order_id, iceberg_qty, recv_window,
                      new_order_resp_type):
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
        .add_optional_params_to_payload(new_client_order_id=new_client_order_id,
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
@click.option("--query", type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
async def account_info(recv_window, query):
    """Get current account information"""
    payload = {
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = Builder(endpoint='api/v3/account', payload=payload) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().filter(query).generate_output()


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
@click.option("--query", type=click.types.STRING)
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


@cli.command("new_oco_order", short_help="Send in a new OCO")
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-lcoid", "--list_client_order_id", type=click.types.STRING)
@click.option("-si", "--side", required=True, callback=validate_side, type=click.types.STRING)
@click.option("-q", "--quantity", required=True, type=click.types.FLOAT)
@click.option("-limcoid", "--limit_client_order_id", type=click.types.STRING)
@click.option("-p", "--price", required=True, type=click.types.FLOAT)
@click.option("-liq", "--limit_iceberg_qty", type=click.types.FLOAT)
@click.option("-scoid", "--stop_client_order_id", type=click.types.STRING)
@click.option("-sp", "--stop_price", required=True, type=click.types.FLOAT)
@click.option("-slp", "--stop_limit_price", type=click.types.FLOAT)
@click.option("-siq", "--stop_iceberg_qty", type=click.types.FLOAT)
@click.option("-sltif", "--stop_limit_time_in_force", callback=validate_time_in_force, type=click.types.STRING)
@click.option("-nort", "--new_order_resp_type", default="FULL", callback=validate_new_order_resp_type,
              type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
@pass_environment
async def new_oco_order(ctx, symbol, list_client_order_id, side, quantity, limit_client_order_id,
                        price, limit_iceberg_qty, stop_client_order_id, stop_price,
                        stop_limit_price, stop_iceberg_qty, stop_limit_time_in_force,
                        new_order_resp_type, recv_window):
    """
    Send in a new OCO.
    
    Other Info:

        Price Restrictions:

            SELL: Limit Price > Last Price > Stop Price

            BUY: Limit Price < Last Price < Stop Price

        Quantity Restrictions:

            Both legs must have the same quantity

            ICEBERG quantities however do not have to be the same.

        Order Rate Limit

            OCO counts as 2 orders against the order rate limit.
    """

    if stop_limit_price is not None and stop_limit_time_in_force is None:
        ctx.log('--stop_limit_time_in_force (-sltif) is required when you sent --stop_limit_price (-slp).')
        return

    payload = {
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'price': price,
        'stopPrice': stop_price,
        'newOrderRespType': new_order_resp_type,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = NewOcoOrderBuilder(endpoint='api/v3/order/oco', method='POST', payload=payload) \
        .add_optional_params_to_payload(list_client_order_id=list_client_order_id,
                                        limit_client_order_id=limit_client_order_id,
                                        limit_iceberg_qty=limit_iceberg_qty,
                                        stop_client_order_id=stop_client_order_id,
                                        stop_limit_price=stop_limit_price,
                                        stop_iceberg_qty=stop_iceberg_qty,
                                        stop_limit_time_in_force=stop_limit_time_in_force) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("cancel_oco_order", short_help="Cancel an entire Order List.")
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-olid", "--order_list_id", type=click.types.INT)
@click.option("-lcoid", "--list_client_order_id", type=click.types.STRING)
@click.option("-ncoid", "--new_client_order_id", type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
@pass_environment
async def cancel_oco_order(ctx, symbol, order_list_id, list_client_order_id,
                           new_client_order_id, recv_window):
    """
    Cancel an entire Order List.

    Weight: 1

    Additional notes:

        Canceling an individual leg will cancel the entire OCO
    """

    if order_list_id is None and list_client_order_id is None:
        ctx.log('Either --order_list_id (-olid) or --list_client_order_id (-lcoid) must be sent.')
        return

    payload = {
        'symbol': symbol,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = CancelOcoOrderBuilder(endpoint='api/v3/orderList', method='DELETE', payload=payload) \
        .add_optional_params_to_payload(order_list_id=order_list_id,
                                        list_client_order_id=list_client_order_id,
                                        new_client_order_id=new_client_order_id) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("oco_order", short_help="Retrieves a specific OCO based on provided optional parameters.")
@click.option("-olid", "--order_list_id", type=click.types.INT)
@click.option("-lcoid", "--list_client_order_id", type=click.types.STRING)
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
@pass_environment
async def oco_order(ctx, order_list_id, list_client_order_id, recv_window):
    """
    Retrieves a specific OCO based on provided optional parameters

    Weight: 1
    """

    if order_list_id is None and list_client_order_id is None:
        ctx.log('Either --order_list_id (-olid) or --list_client_order_id (-lcoid) must be sent.')
        return

    payload = {
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = OcoOrderBuilder(endpoint='api/v3/orderList', payload=payload) \
        .add_optional_params_to_payload(order_list_id=order_list_id,
                                        list_client_order_id=list_client_order_id) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("all_oco_orders", short_help="Retrieves all OCO based on provided optional parameters.")
@click.option("-fid", "--from_id", type=click.types.INT)
@click.option("-st", "--start_time", type=click.types.INT)
@click.option("-et", "--end_time", type=click.types.INT)
@click.option("-l", "--limit", default=500, show_default=True, type=click.types.IntRange(1, 1000))
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
async def all_oco_orders(from_id, start_time, end_time, limit, recv_window):
    """
    Retrieves all OCO based on provided optional parameters.

    Weight: 10
    """
    payload = {
        'limit': limit,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = AllOcoOrderBuilder(endpoint='api/v3/allOrderList', payload=payload) \
        .add_optional_params_to_payload(from_id=from_id,
                                        start_time=start_time,
                                        end_time=end_time) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("open_oco_orders")
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@coro
async def open_oco_orders(recv_window):
    """
    Weight: 2
    """
    payload = {
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = Builder(endpoint='api/v3/openOrderList', payload=payload).set_security()

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("my_trades", short_help="Get trades for a specific account and symbol.")
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-st", "--start_time", type=click.types.INT)
@click.option("-et", "--end_time", type=click.types.INT)
@click.option("-fid", "--from_id", type=click.types.INT)
@click.option("-l", "--limit", default=500, show_default=True, type=click.types.IntRange(1, 1000))
@click.option("-rw", "--recv_window", default=5000, show_default=True, callback=validate_recv_window,
              type=click.types.INT)
@click.option("--query", type=click.types.STRING)
@coro
async def my_trades(symbol, start_time, end_time, from_id, limit, recv_window, query):
    """
    Get trades for a specific account and symbol.

    Weight: 5

    NOTES:

        If fromId is set, it will get id >= that fromId. Otherwise most recent trades are returned.
    """
    payload = {
        'symbol': symbol,
        'limit': limit,
        'recvWindow': recv_window,
        'timestamp': get_timestamp()
    }

    builder = MyTradesBuilder(endpoint='api/v3/myTrades', payload=payload) \
        .add_optional_params_to_payload(start_time=start_time,
                                        end_time=end_time,
                                        from_id=from_id) \
        .set_security()

    await builder.send_http_req()

    builder.handle_response().filter(query).generate_output()
