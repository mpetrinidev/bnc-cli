import json
import yaml

from pandas import json_normalize

from src.cli import pass_environment


def json_to_str(value, indent: int = 2):
    return json.dumps(value, indent=indent)


def json_to_table(value):
    return json_normalize(value, "balances", ['asset', 'free', 'locked'])


def to_query_string_parameters(values: {}) -> str:
    if not values:
        raise ValueError('values cannot be empty')

    return '&'.join(key + '=' + str(val) for key, val in values.items())


@pass_environment
def generate_output(ctx, values):
    output = None

    if ctx.output == 'json':
        output = json_to_str(values)

    if ctx.output == 'yaml':
        output = yaml.safe_dump(values, default_flow_style=False, sort_keys=False)

    ctx.log(output)
