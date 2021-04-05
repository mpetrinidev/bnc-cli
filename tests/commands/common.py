import json


def read_json_test_file(name):
    with open(name) as json_file:
        response = json.load(json_file)

        return response
