from abc import abstractmethod

import click
import requests_async as requests
import yaml
import jmespath

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

    @abstractmethod
    def add_optional_params_to_payload(self, **kwargs):
        pass

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
                f'Binance API is reporting the following error: {result["results"]["code"]} | '
                f'{result["results"]["msg"]}')
            self.has_error = True

        self.result = result

        return self

    def filter(self, query):
        if self.has_error:
            return self

        if query is not None:
            self.result['results'] = jmespath.search(query, self.result['results'])

        return self

    def generate_output(self):
        if self.has_error:
            return self

        output = None

        if self.env.output == 'json':
            output = json_to_str(self.result['results'])

        if self.env.output == 'yaml':
            output = yaml.safe_dump(self.result['results'], default_flow_style=False, sort_keys=False)

        self.env.log(output)


class LimitOrderBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        quote_order_qty, new_client_order_id, stop_price, iceberg_qty = kwargs.values()

        if quote_order_qty is not None:
            self.payload['quoteOrderQty'] = quote_order_qty

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if stop_price is not None:
            self.payload['stopPrice'] = stop_price

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class MarketOrderBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        quantity, time_in_force, \
        quote_order_qty, price, \
        new_client_order_id, stop_price, \
        iceberg_qty = kwargs.values()

        if quantity is not None:
            self.payload['quantity'] = quantity

        if time_in_force is not None:
            self.payload['timeInForce'] = time_in_force

        if quote_order_qty is not None:
            self.payload['quoteOrderQty'] = quote_order_qty

        if price is not None:
            self.payload['price'] = price

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if stop_price is not None:
            self.payload['stopPrice'] = stop_price

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class StopLossBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        time_in_force, quote_order_qty, \
        price, new_client_order_id, \
        iceberg_qty = kwargs.values()

        if time_in_force is not None:
            self.payload['timeInForce'] = time_in_force

        if quote_order_qty is not None:
            self.payload['quoteOrderQty'] = quote_order_qty

        if price is not None:
            self.payload['price'] = price

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class StopLossLimitBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        quote_order_qty, new_client_order_id, iceberg_qty = kwargs.values()

        if quote_order_qty is not None:
            self.payload['quoteOrderQty'] = quote_order_qty

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class TakeProfitBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        time_in_force, quote_order_qty, \
        price, new_client_order_id, \
        iceberg_qty = kwargs.values()

        if time_in_force is not None:
            self.payload['timeInForce'] = time_in_force

        if quote_order_qty is not None:
            self.payload['quoteOrderQty'] = quote_order_qty

        if price is not None:
            self.payload['price'] = price

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class TakeProfitLimitBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        quote_order_qty, \
        new_client_order_id, \
        iceberg_qty = kwargs.values()

        if quote_order_qty is not None:
            self.payload['quoteOrderQty'] = quote_order_qty

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class LimitMakerBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        time_in_force, quote_order_qty, \
        stop_price, new_client_order_id, \
        iceberg_qty = kwargs.values()

        if time_in_force is not None:
            self.payload['timeInForce'] = time_in_force

        if quote_order_qty is not None:
            self.payload['quoteOrderQty'] = quote_order_qty

        if stop_price is not None:
            self.payload['stopPrice'] = stop_price

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class CancelOrderBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        order_id, orig_client_order_id, new_client_order_id = kwargs.values()

        if order_id is not None:
            self.payload['orderId'] = order_id

        if orig_client_order_id is not None:
            self.payload['origClientOrderId'] = orig_client_order_id

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        return self


class AccountInfoBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        pass

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


class OpenOrdersBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        symbol = kwargs['symbol']

        if symbol is not None:
            self.payload['symbol'] = symbol

        return self


class OrderStatusBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        order_id, orig_client_order_id = kwargs.values()

        if order_id is not None:
            self.payload['orderId'] = order_id

        if orig_client_order_id is not None:
            self.payload['origClientOrderId'] = orig_client_order_id

        return self


class KlinesBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        start_time, end_time, limit = kwargs.values()

        if start_time is not None:
            self.payload['startTime'] = start_time

        if end_time is not None:
            self.payload['endTime'] = end_time

        if limit is not None:
            self.payload['limit'] = limit

        return self


class Ticker24AndPriceBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        symbol = kwargs['symbol']

        if symbol is not None:
            self.payload = {'symbol': symbol}

        return self


class AllOrderBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        order_id, start_time, end_time = kwargs.values()

        if order_id is not None:
            self.payload['orderId'] = order_id

        if start_time is not None:
            self.payload['startTime'] = start_time

        if end_time is not None:
            self.payload['endTime'] = end_time

        return self


class MyTradesBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        start_time, end_time, from_id = kwargs.values()

        if start_time is not None:
            self.payload['startTime'] = start_time

        if end_time is not None:
            self.payload['endTime'] = end_time

        if from_id is not None:
            self.payload['fromId'] = from_id

        return self
