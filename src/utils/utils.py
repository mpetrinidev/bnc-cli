import json


def json_to_str(value, indent: int = 2):
    return json.dumps(value, indent=indent)


def to_query_string_parameters(values: {}) -> str:
    if not values:
        raise ValueError('values cannot be empty')

    return '&'.join(key + '=' + str(val) for key, val in values.items())
