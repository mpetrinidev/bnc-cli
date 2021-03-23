import click

from src.builder import Builder
from src.cli import pass_environment
from src.decorators import coro
from src.validation.val_market import validate_limit


@click.group(short_help='Market data endpoints')
def cli():
    """
    Market data endpoints
    """
    pass


@cli.command("test", short_help='Test connectivity to the Rest API.')
@pass_environment
@coro
async def test(ctx):
    """Test connectivity to the Rest API."""
    builder = Builder(endpoint='api/v3/ping').set_security()
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
    builder = Builder(endpoint='api/v3/time').set_security()
    await builder.send_http_req()

    builder.handle_response()

    if not builder.result['successful']:
        return

    ctx.log('Binance API is up and running')

    builder.generate_output()


@cli.command("exchange_info", short_help='Current exchange trading rules and symbol information.')
@coro
async def exchange_info():
    """Current exchange trading rules and symbol information."""
    builder = Builder(endpoint='api/v3/exchangeInfo').set_security()
    await builder.send_http_req()

    builder.handle_response().generate_output()


@cli.command("trades", short_help='Get recent trades.')
@click.option("-sy", "--symbol", required=True, type=click.types.STRING)
@click.option("-l", "--limit", default=500, show_default=True, callback=validate_limit, type=click.types.INT)
@coro
async def trades(symbol, limit):
    """Get recent trades."""
    payload = {
        'symbol': symbol,
        'limit': limit
    }

    builder = Builder(endpoint='api/v3/trades', payload=payload, without_signature=True).set_security()
    await builder.send_http_req()

    builder.handle_response().generate_output()
