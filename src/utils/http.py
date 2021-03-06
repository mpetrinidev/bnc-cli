from src.cli import pass_environment


@pass_environment
def handle_response(ctx, r):
    result = {
        'successful': False,
        'status_code': r.status_code,
        'results': r.json(),
        'headers': r.headers
    }

    if 200 <= r.status_code <= 299:
        result['successful'] = True

    if 500 <= r.status_code <= 599:
        ctx.log("Binance's side internal error has occurred")

    if 400 <= r.status_code <= 499:
        ctx.log(f'Binance API is reporting the following error: {result["results"]["code"]} | {result["results"]["msg"]}')

    return result
