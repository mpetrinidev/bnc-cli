import requests

from src.utils.globals import *
from src.utils.security import Security
from src.utils.utils import Utils
from src.utils.api_time import ApiTime


# Command: bnc spot <method_name>
class Spot:
    def __init__(self):
        pass

    def validate_account_info(self, params):
        if 'recv_window' not in params:
            params['recv_window'] = 5_000

        if 'recv_window' in params and int(params['recv_window']) > 60_000:
            raise ValueError('recv_window cannot exceed 60_000')

        if 'locked_free' in params:
            locked_free = str(params['locked_free']).upper()

            if locked_free != 'L' or locked_free != 'F' or locked_free != 'B':
                raise ValueError('locked_free incorrect value. Possible values: L | F | B')

    def account_info(self, **kwargs):
        self.validate_account_info(kwargs)

        payload = {'recvWindow': kwargs['recv_window'], 'timestamp': ApiTime.get_timestamp()}
        total_params = Utils.to_query_string_parameters(payload)

        payload['signature'] = Security.get_hmac_hash(total_params, Security.get_secret_key())

        headers = Security.get_api_key_header()
        r = requests.get(API_BINANCE + 'api/v3/account', headers=headers, params=payload)

        if r.status_code != 200:
            yield 'Wrong request: status_code: ' + str(r.status_code)
            return

        results = r.json()
        results['balances'] = [x for x in results['balances'] if float(x['free']) > 0.0 or float(x['locked']) > 0.0]

        return results
