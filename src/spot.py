import requests_async as requests

from src.utils.globals import *
from src.utils.security import Security
from src.utils.utils import Utils
from src.utils.api_time import ApiTime


# Command: bnc spot <method_name>
class Spot:
    def __init__(self):
        pass

    async def account_info(self, **kwargs):
        self.validate_account_info(kwargs)

        payload = {'recvWindow': kwargs['recv_window'], 'timestamp': ApiTime.get_timestamp()}
        total_params = Utils.to_query_string_parameters(payload)

        payload['signature'] = Security.get_hmac_hash(total_params, Security.get_secret_key())

        headers = Security.get_api_key_header()
        r = await requests.get(API_BINANCE + 'api/v3/account', headers=headers, params=payload)

        if r.status_code != 200:
            return 'Wrong request: status_code: ' + str(r.status_code)

        results = r.json()
        results['balances'] = self.filter_balances_account_info(results['balances'], kwargs)

        return results

    def filter_balances_account_info(self, balances, filters):
        if 'locked_free' in filters:
            locked_free = str(filters['locked_free']).upper()

            if locked_free == 'B':
                balances = [x for x in balances if float(x['free']) > 0.0 or float(x['locked']) > 0.0]
            elif locked_free == 'F':
                balances = [x for x in balances if float(x['free']) > 0.0]
            elif locked_free == 'L':
                balances = [x for x in balances if float(x['locked']) > 0.0]

        return balances

    def validate_account_info(self, params):
        if 'recv_window' not in params:
            params['recv_window'] = 5_000

        if 'recv_window' in params and int(params['recv_window']) > 60_000:
            raise ValueError('recv_window cannot exceed 60_000')

        if 'locked_free' in params:
            locked_free = str(params['locked_free']).upper()

            if locked_free not in ['L', 'F', 'B']:
                raise ValueError('locked_free incorrect value. Possible values: L | F | B')
