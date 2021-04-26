import click


def validate_interval(ctx, param, value):
    if value not in ["1m", "3m", "5m", "15m", "30m", "1h",
                     "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]:
        raise click.BadParameter(f'{value}. Possible values: 1m | 3m | 5m | 15m | 30m | 1h | 2h | 4h | 6h | 8h | 12h '
                                 f'| 1d | 3d | 1w | 1M')

    return value
