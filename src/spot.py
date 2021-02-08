import requests

from utils.globals import *
from utils.security import Security
from utils.utils import Utils
from utils.api_time import ApiTime


# Command: bnc spot <method_name>
class Spot:
    def __init__(self):
        pass

    def validate(self, params):
        if 'recvWindow' not in params:
            params['recvWindow'] = 5000

        if 'recvWindow' in params and params['recvWindow'] > 60000:
            raise ValueError('recvWindow cannot exceed 60_000')

        if 'locked_free' in params and (params['locked_free'] != 'L' or
                                        params['locked_free'] != 'F' or
                                        params['locked_free'] != 'B'):
            raise ValueError('locked_free incorrect value. Possible values: L | F | B')

    def account_info(self, **kwargs):
        self.validate(kwargs)

        payload = {'recvWindow': kwargs['recvWindow'], 'timestamp': ApiTime.get_timestamp()}
        total_params = Utils.to_query_string_parameters(payload)

        payload['signature'] = Security.get_hmac_hash(total_params)

        headers = Security.get_api_key_header()
        r = requests.get(API_BINANCE + 'api/v3/account', headers=headers, params=payload)

        results = r.json()
        results['balances'] = [x for x in results['balances'] if float(x['free']) > 0.0 or float(x['locked']) > 0.0]

        return results
