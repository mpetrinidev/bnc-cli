import json


def json_to_str(value, indent: int = 2):
    return json.dumps(value, indent=indent)


def to_query_string_parameters(values: {}) -> str:
    if not values:
        raise ValueError('values cannot be empty')

    return '&'.join(key + '=' + str(val) for key, val in values.items())


def to_log_str(dic: {}) -> str:
    if not dic:
        raise ValueError('dic cannot be empty')

    return ' '.join(key + "=" + str(val) for key, val in dic.items())


def mask_dic_values(dic: {}, keys):
    if not dic:
        raise ValueError('dic cannot be empty')

    if keys is None:
        raise ValueError('keys cannot be null')

    if len(keys) == 0:
        raise ValueError('keys cannot be empty')

    new_dic = dict(dic)

    for key in dic:
        if key not in keys:
            continue

        new_dic[key] = '#' * (len(dic[key]) // 2)

    return new_dic
