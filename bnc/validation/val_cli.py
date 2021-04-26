import click


def validate_output_value(ctx, param, value):
    value = str(value).lower()
    if value not in ['json', 'table', 'yaml']:
        raise click.BadParameter(value + '. Possible values: json | table | yaml')

    return value
