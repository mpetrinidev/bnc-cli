import click


def validate_limit(ctx, param, value):
    if value is None:
        return

    value = int(value)
    if value not in [5, 10, 20, 50, 100, 500, 1000, 5000]:
        raise click.BadParameter(f'{value}' + '. Possible values: 5 | 10 | 20 | 50 | 100 | 500 | 1000 | 5000')

    return value
