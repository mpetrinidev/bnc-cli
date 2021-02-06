import fire
import requests

from utils.security import Security
from utils.utils import Utils
from utils.api_time import ApiTime

API_BINANCE = 'https://api.binance.com/api/v3/account'


class Bnc:
    def __init__(self):
        pass

    def spot_account(self, recvWindow: int = 5000):
        payload = {'recvWindow': recvWindow, 'timestamp': ApiTime.get_timestamp()}
        total_params = Utils.to_query_string_parameters(payload)

        payload['signature'] = Security.get_hmac_hash(total_params)

        headers = Security.get_api_key_header()
        r = requests.get(API_BINANCE, headers=headers, params=payload)

        results = r.json()
        results['balances'] = [x for x in results['balances'] if float(x['free']) > 0.0 or float(x['locked']) > 0.0]

        return results


if __name__ == '__main__':
    fire.Fire(Bnc)
