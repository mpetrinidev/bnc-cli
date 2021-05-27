import json


def read_json_test_file(name):
    with open(name) as json_file:
        response = json.load(json_file)

        return response


def get_headers():
    return {
        'content-type': 'json',
        'x-mbx-uuid': 'uuid',
        'x-mbx-used-weight': 10,
        'x-mbx-used-weight-1m': 1
    }
