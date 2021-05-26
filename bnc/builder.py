import datetime
from abc import abstractmethod

import click
import requests_async as requests
import yaml
import jmespath

from .environment import Environment
from .utils.config import read_configuration

from .utils.security import get_api_key_header
from .utils.security import get_hmac_hash
from .utils.security import get_secret_key

from .utils.utils import to_query_string_parameters, mask_dic_values
from .utils.utils import json_to_str


class Builder:
    def __init__(self, endpoint: str, payload: {} = None, method: str = 'GET', headers=None, without_signature=False):
        if headers is None:
            headers = {}

        if endpoint is None or len(endpoint) == 0:
            raise ValueError('endpoint cannot be null or empty')

        self.without_signature = without_signature
        self.payload = payload

        self.method = method.upper()
        self.__validate_http_method__()

        self.headers = headers

        self.response = None
        self.result = None
        self.has_error = False

        self.config_values = read_configuration()

        self.endpoint = self.config_values['bnc_api_endpoint'] + endpoint

        self.headers['User-Agent'] = f'bnc-cli {"" if not self.config_values["is_testnet"] else "- testnet"} ' \
                                     f'(https://github.com/mpetrinidev/bnc-cli)'

        ctx = click.get_current_context(silent=True)
        self.env = None

        if ctx is not None:
            self.env = ctx.ensure_object(Environment)

        self.__verbose_constructor_values__()

    def __verbose_constructor_values__(self):
        self.env.logger.info(f'Initial values', extra={
            'endpoint': self.endpoint,
            'without_signature': self.without_signature,
            'payload': self.payload,
            'method': self.method,
            'headers': self.headers
        })

    def __validate_http_method__(self):
        if self.method.upper() not in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']:
            raise ValueError('Http method is invalid')

    @abstractmethod
    def add_optional_params_to_payload(self, **kwargs):
        pass

    def set_security(self):
        if self.payload is not None and not self.without_signature:
            self.payload['signature'] = get_hmac_hash(to_query_string_parameters(self.payload), get_secret_key())
            self.env.logger.info(f'Signature created successfully')

        self.headers.update(get_api_key_header())
        self.env.logger.info(f'Headers updated successfully at set_security',
                             extra={'headers': mask_dic_values(self.headers, ['X-MBX-APIKEY'])})

        return self

    async def send_http_req(self):
        self.env.logger.debug('Starting HTTP call to Binance API')

        if self.method == 'GET':
            self.response = await requests.get(self.endpoint, headers=self.headers, params=self.payload)

        if self.method == 'POST':
            self.response = await requests.post(self.endpoint, headers=self.headers, params=self.payload)

        if self.method == 'DELETE':
            self.response = await requests.delete(self.endpoint, headers=self.headers, params=self.payload)

        self.env.logger.debug('Finishing HTTP call to Binance API')
        self.env.logger.info('Response details', extra={
            'status_code': self.response.__dict__['status_code'],
            'content-type': self.response.__dict__['headers']['content-type'],
            'x-mbx-uuid': self.response.__dict__['headers']['x-mbx-uuid'],
            'x-mbx-used-weight': self.response.__dict__['headers']['x-mbx-used-weight'],
            'x-mbx-used-weight-1m': self.response.__dict__['headers']['x-mbx-used-weight-1m'],
            'time-taken': str(self.response.__dict__['elapsed'])
        })

        return self

    def handle_response(self):
        result = {
            'successful': False,
            'status_code': self.response.status_code,
            'results': self.response.json(),
            'headers': self.response.headers
        }

        self.env.logger.debug('Processing response...')

        if 200 <= self.response.status_code <= 299:
            self.env.logger.info('Everything looks good')

            result['successful'] = True

        if 500 <= self.response.status_code <= 599:
            self.env.logger.error('HTTP Response error (500 - 599)')

            self.env.log("Binance's side internal error has occurred")
            self.has_error = True

        if 400 <= self.response.status_code <= 499:
            self.env.logger.error('HTTP Response error (400-499)', extra={
                'code': result['results']['code'],
                'msg': result['results']['msg']
            })

            self.env.log(
                f'Binance API is reporting the following error: {result["results"]["code"]} | '
                f'{result["results"]["msg"]}')
            self.has_error = True

        self.result = result

        self.env.logger.debug('Finishing process response')

        return self

    def filter(self, query):
        if self.has_error:
            return self

        self.env.logger.debug('Applying filter to results')

        if query is not None:
            self.result['results'] = jmespath.search(query, self.result['results'])
        else:
            self.env.logger.info('No filter provided')

        self.env.logger.debug('Ending filtering results')

        return self

    def generate_output(self):
        if self.has_error:
            return self

        output = None

        self.env.logger.info(f'Generating output in {self.env.output} format')

        if self.env.output == 'json':
            output = json_to_str(self.result['results'])

        if self.env.output == 'yaml':
            output = yaml.safe_dump(self.result['results'], default_flow_style=False, sort_keys=False)

        self.env.logger.info(f'Output generated successfully')

        self.env.log(output)


class LimitOrderBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        new_client_order_id, iceberg_qty = kwargs.values()

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class MarketOrderBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        quantity, quote_order_qty, \
        new_client_order_id = kwargs.values()

        if quantity is not None:
            self.payload['quantity'] = quantity

        if quote_order_qty is not None:
            self.payload['quoteOrderQty'] = quote_order_qty

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        return self


class StopLossLimitBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        new_client_order_id, iceberg_qty = kwargs.values()

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class TakeProfitLimitBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        new_client_order_id, \
        iceberg_qty = kwargs.values()

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        if iceberg_qty is not None:
            self.payload['icebergQty'] = iceberg_qty

        return self


class LimitMakerBuilder(Builder):

    def add_optional_params_to_payload(self, **kwargs):
        new_client_order_id, \
        iceberg_qty = kwargs.values()

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


class NewOcoOrderBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        list_client_order_id, limit_client_order_id, \
        limit_iceberg_qty, stop_client_order_id, \
        stop_limit_price, stop_iceberg_qty, \
        stop_limit_time_in_force = kwargs.values()

        if list_client_order_id is not None:
            self.payload['listClientOrderId'] = list_client_order_id

        if limit_client_order_id is not None:
            self.payload['limitClientOrderId'] = limit_client_order_id

        if limit_iceberg_qty is not None:
            self.payload['limitIcebergQty'] = limit_iceberg_qty

        if stop_client_order_id is not None:
            self.payload['stopClientOrderId'] = stop_client_order_id

        if stop_limit_price is not None:
            self.payload['stopLimitPrice'] = stop_limit_price

        if stop_iceberg_qty is not None:
            self.payload['stopIcebergQty'] = stop_iceberg_qty

        if stop_limit_time_in_force is not None:
            self.payload['stopLimitTimeInForce'] = stop_limit_time_in_force

        return self


class CancelOcoOrderBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        order_list_id, list_client_order_id, new_client_order_id = kwargs.values()

        if order_list_id is not None:
            self.payload['orderListId'] = order_list_id

        if list_client_order_id is not None:
            self.payload['listClientOrderId'] = list_client_order_id

        if new_client_order_id is not None:
            self.payload['newClientOrderId'] = new_client_order_id

        return self


class OcoOrderBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        order_list_id, list_client_order_id = kwargs.values()

        if order_list_id is not None:
            self.payload['orderListId'] = order_list_id

        if list_client_order_id is not None:
            self.payload['origClientOrderId'] = list_client_order_id

        return self


class AllOcoOrderBuilder(Builder):
    def add_optional_params_to_payload(self, **kwargs):
        from_id, start_time, end_time = kwargs.values()

        if from_id is not None:
            self.payload['fromId'] = from_id
            return self

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
