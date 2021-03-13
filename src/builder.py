from abc import abstractmethod

import click
import requests_async as requests
import yaml

from src.cli import Environment
from src.utils.globals import API_BINANCE
from src.utils.security import get_api_key_header, get_hmac_hash, get_secret_key
from src.utils.utils import to_query_string_parameters, json_to_str


class Builder:
    def __init__(self, endpoint, payload, method: str = 'GET'):
        self.payload = payload
        self.endpoint = endpoint
        self.method = method
        self.headers = None
        self.response = None
        self.result = None
        self.has_error = False

        ctx = click.get_current_context()
        self.env = ctx.ensure_object(Environment)

    def set_security(self):
        self.payload['signature'] = get_hmac_hash(to_query_string_parameters(self.payload), get_secret_key())
        self.headers = get_api_key_header()

        return self

    async def send_http_req(self):
        if self.method == 'GET':
            self.response = await requests.get(API_BINANCE + self.endpoint, headers=self.headers, params=self.payload)

        if self.method == 'POST':
            self.response = await requests.post(API_BINANCE + self.endpoint, headers=self.headers, params=self.payload)

        return self

    def handle_response(self):
        result = {
            'successful': False,
            'status_code': self.response.status_code,
            'results': self.response.json(),
            'headers': self.response.headers
        }

        if 200 <= self.response.status_code <= 299:
            result['successful'] = True

        if 500 <= self.response.status_code <= 599:
            self.env.log("Binance's side internal error has occurred")
            self.has_error = True

        if 400 <= self.response.status_code <= 499:
            self.env.log(
                f'Binance API is reporting the following error: {result["results"]["code"]} | {result["results"]["msg"]}')
            self.has_error = True

        self.result = result

        return self

    def generate_output(self):
        if self.has_error:
            return

        output = None

        if self.env.output == 'json':
            output = json_to_str(self.result['results'])

        if self.env.output == 'yaml':
            output = yaml.safe_dump(self.result['results'], default_flow_style=False, sort_keys=False)

        self.env.log(output)
