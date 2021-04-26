import click


def validate_recv_window(ctx, param, value):
    if int(value) > 60000:
        raise click.BadParameter(str(value) + '. Cannot exceed 60000')

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


def validate_new_order_resp_type(ctx, param, value):
    value = str(value).upper()

    if value not in ['FULL', 'ACK', 'RESULT']:
        raise click.BadParameter(value + '. Possible values: FULL | ACK | RESULT')

    return value
