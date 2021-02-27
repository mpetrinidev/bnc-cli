from src.cli import pass_environment


@pass_environment
def handle_response(ctx, r):
    if 200 <= r.status_code <= 299:
        return True, r.json(), r.headers

    if 500 <= r.status_code <= 599:
        ctx.log("Binance's side internal error has occurred")
        return

    if 400 <= r.status_code <= 499:
        result = r.json()

        ctx.log(f'Binance API is reporting the following error: ({result["code"]} | {result["msg"]})')
        ctx.log(r.status_code)

        return False, result, r.headers
