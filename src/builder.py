from abc import abstractmethod

import click
import requests_async as requests
import yaml

from src.cli import Environment
from src.utils.globals import API_BINANCE
from src.utils.security import get_api_key_header, get_hmac_hash, get_secret_key
from src.utils.utils import to_query_string_parameters, json_to_str


class Builder:
    def __init__(self, endpoint: str, payload: {} = None, method: str = 'GET', headers=None, without_signature=False):
        if headers is None:
            headers = {}

        if endpoint is None or len(endpoint) == 0:
            raise ValueError('endpoint cannot be null or empty')

        self.without_signature = without_signature
        self.payload = payload
        self.endpoint = endpoint

        self._validate_http_method(method)

        self.method = method.upper()
        self.headers = headers

        self.response = None
        self.result = None
        self.has_error = False

        ctx = click.get_current_context(silent=True)
        self.env = None

        if ctx is not None:
            self.env = ctx.ensure_object(Environment)

    def _validate_http_method(self, method: str):
        if method.upper() not in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']:
            raise ValueError('Http method is invalid')

    def set_security(self):
        if self.payload is not None and not self.without_signature:
            self.payload['signature'] = get_hmac_hash(to_query_string_parameters(self.payload), get_secret_key())

        self.headers.update(get_api_key_header())

        return self

    async def send_http_req(self):
        if self.method == 'GET':
            self.response = await requests.get(API_BINANCE + self.endpoint, headers=self.headers, params=self.payload)

        if self.method == 'POST':
            self.response = await requests.post(API_BINANCE + self.endpoint, headers=self.headers, params=self.payload)

        if self.method == 'DELETE':
            self.response = await requests.delete(API_BINANCE + self.endpoint, headers=self.headers,
                                                  params=self.payload)

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

    @abstractmethod
    def filter(self, **kwargs):
        if self.has_error:
            return self

        pass

    def generate_output(self):
        if self.has_error:
            return self

        output = None

        if self.env.output == 'json':
            output = json_to_str(self.result['results'])

        if self.env.output == 'yaml':
            output = yaml.safe_dump(self.result['results'], default_flow_style=False, sort_keys=False)

        self.env.log(output)


class AccountInfoBuilder(Builder):
    def filter(self, **kwargs):
        if self.has_error:
            return self

        if 'locked_free' in kwargs and kwargs['locked_free'] is not None:
            locked_free = str(kwargs['locked_free']).upper()

            if self.result['results']['balances'] is None:
                self.result['results']['balances'] = []
                return self

            if len(self.result['results']['balances']) == 0:
                return self

            filter_func = None

            if locked_free == 'B':
                filter_func = lambda balances: [x for x in balances if
                                                float(x['free']) > 0.0 or float(x['locked']) > 0.0]
            elif locked_free == 'F':
                filter_func = lambda balances: [x for x in balances if float(x['free']) > 0.0]
            elif locked_free == 'L':
                filter_func = lambda balances: [x for x in balances if float(x['locked']) > 0.0]

            self.result['results']['balances'] = filter_func(self.result['results']['balances'])

        return self
