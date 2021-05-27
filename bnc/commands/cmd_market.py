import click

from ..builder import Builder
from ..builder import KlinesBuilder
from ..builder import Ticker24AndPriceBuilder

from ..environment import pass_environment

from ..decorators import coro
from ..validation.val_market import validate_interval


@click.group(short_help='Market data endpoints')
def cli():
    """Market data endpoints"""


@cli.command("test", short_help='Test connectivity to the Rest API.')
@pass_environment
@coro
async def test(ctx):
    """Test connectivity to the Rest API."""
    builder = Builder(endpoint='api/v3/ping')
    await builder.send_http_req()

    builder.handle_response()

    if not builder.result['successful']:
        return

    ctx.log('Binance API is up and running')


@cli.command("server_time", short_help='Test connectivity to the Rest API and get the current server time.')
@pass_environment
@coro
async def server_time(ctx):
    """Test connectivity to the Rest API and get the current server time."""
    builder = Builder(endpoint='api/v3/time')
    await builder.send_http_req()

    builder.handle_response()

    if not builder.result['successful']:
        return

    ctx.log('Binance API is up and running')

    builder.generate_output()


@cli.command("exchange_info", short_help='Current exchange trading rules and symbol information.')
@click.option("--query", type=click.types.STRING)
@coro
async def exchange_info(query):
    """Current exchange trading rules and symbol information."""
    builder = Builder(endpoint='api/v3/exchangeInfo')
    await builder.send_http_req()

    builder.handle_response().filter(query).generate_output()


@cli.command("trades", short_help='Get recent trades.')
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-l", "--limit", default=500, show_default=True, type=click.types.IntRange(1, 1000))
@coro
async def trades(symbol, limit):
    """Get recent trades."""
    payload = {
        'symbol': symbol,
        'limit': limit
    }

    builder = Builder(endpoint='api/v3/trades', payload=payload, without_signature=True)
    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("klines", short_help="Kline/candlestick bars for a symbol. "
                                  "Klines are uniquely identified by their open time.")
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-i", "--interval", required=True, callback=validate_interval, type=click.types.STRING)
@click.option("-st", "--start_time", type=click.types.INT)
@click.option("-et", "--end_time", type=click.types.INT)
@click.option("-l", "--limit", default=500, show_default=True, type=click.types.IntRange(1, 1000))
@coro
async def klines(symbol, interval, start_time, end_time, limit):
    """
    Kline/candlestick bars for a symbol.

    Klines are uniquely identified by their open time.

    NOTE: If start_time and end_time are not sent, the most recent klines are returned.
    """
    payload = {
        'symbol': symbol,
        'interval': str(interval).lower()
    }

    builder = KlinesBuilder(endpoint='api/v3/klines', payload=payload, without_signature=True) \
        .add_optional_params_to_payload(start_time=start_time,
                                        end_time=end_time,
                                        limit=limit)

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("current_avg_price", short_help="Current average price for a symbol.")
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@coro
async def current_avg_price(symbol):
    """
    Current average price for a symbol.
    """
    payload = {
        'symbol': symbol
    }

    builder = Builder(endpoint='api/v3/avgPrice', payload=payload, without_signature=True)

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("ticker_24hr", short_help="24 hour rolling window price change statistics. "
                                       "Careful when accessing this with no symbol.")
@click.option("-sy", "--symbol", type=click.types.STRING)
@coro
async def ticker_24hr(symbol):
    """
    24 hour rolling window price change statistics. Careful when accessing this with no symbol.

    NOTE:
        Weight: 1 for a single symbol;
        40 when the symbol parameter is omitted;
    """
    builder = Ticker24AndPriceBuilder(endpoint='api/v3/ticker/24hr', without_signature=True) \
        .add_optional_params_to_payload(symbol=symbol)

    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("ticker_price", short_help="Latest price for a symbol or symbols.")
@click.option("-sy", "--symbol", type=click.types.STRING)
@coro
async def ticker_price(symbol):
    """
    Latest price for a symbol or symbols.

    NOTE:
        Weight: 1 for a single symbol;
        2 when the symbol parameter is omitted;
    """
    builder = Ticker24AndPriceBuilder(endpoint='api/v3/ticker/price', without_signature=True) \
        .add_optional_params_to_payload(symbol=symbol)

    await builder.send_http_req()

    builder.handle_response().generate_output()
