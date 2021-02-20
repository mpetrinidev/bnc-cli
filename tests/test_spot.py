from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from src.commands.cmd_spot import account_info


class TestSpot(TestCase):
    def setUp(self) -> None:
        pass

    def test_validate_account_info_recv_window_greater_than_60000(self):
        params = {'recv_window': 60_001}
        self.assertRaisesRegex(ValueError, 'recv_window cannot exceed 60_000', account_info, params)

    def test_validate_account_info_recv_window_is_str_and_greater_than_60000(self):
        params = {'recv_window': '60_001'}
        self.assertRaisesRegex(ValueError, 'recv_window cannot exceed 60_000', account_info, params)

    def test_validate_account_info_locked_free_incorrect_value(self):
        params = {'locked_free': 'G'}
        self.assertRaisesRegex(ValueError, 'locked_free incorrect value. Possible values: L | F | B',
                               account_info, params)


class TestSpotAsync(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.account_info = {
            "makerCommission": 15,
            "takerCommission": 15,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": True,
            "canWithdraw": True,
            "canDeposit": True,
            "updateTime": 123456789,
            "accountType": "SPOT",
            "balances": [
                {
                    "asset": "BTC",
                    "free": "4723846.89208129",
                    "locked": "0.00000000"
                },
                {
                    "asset": "ETH",
                    "free": "0.00000000",
                    "locked": "0.00000000"
                },
                {
                    "asset": "BNB",
                    "free": "0.00000000",
                    "locked": "10.250"
                }
            ]
        }

    @patch('src.spot.requests.get')
    @patch('src.spot.Security.get_api_key_header')
    @patch('src.spot.Security.get_secret_key')
    async def test_account_info_all_properties(self, mock_get_secret_key, mock_get_api_key_header, mock_request_get):
        self.mock_account_info(mock_get_api_key_header, mock_get_secret_key, mock_request_get)

        params = {'recv_window': 5000}
        results = await account_info.account_info(**params)

        self.assertIsNotNone(results)
        self.assertDictEqual(account_info, results)

    @patch('src.spot.requests.get')
    @patch('src.spot.Security.get_api_key_header')
    @patch('src.spot.Security.get_secret_key')
    async def test_account_info_locked_balances(self, mock_get_secret_key, mock_get_api_key_header, mock_request_get):
        self.mock_account_info(mock_get_api_key_header, mock_get_secret_key, mock_request_get)

        params = {'locked_free': 'L'}
        results = await account_info.account_info(**params)

        self.assertIsNotNone(results)
        self.assertEqual(1, len(results['balances']))
        self.assertEqual("BNB", results['balances'][0]['asset'])
        self.assertEqual("0.00000000", results['balances'][0]['free'])
        self.assertEqual("10.250", results['balances'][0]['locked'])

    @patch('src.spot.requests.get')
    @patch('src.spot.Security.get_api_key_header')
    @patch('src.spot.Security.get_secret_key')
    async def test_account_info_free_balances(self, mock_get_secret_key, mock_get_api_key_header, mock_request_get):
        self.mock_account_info(mock_get_api_key_header, mock_get_secret_key, mock_request_get)

        params = {'locked_free': 'F'}
        results = await account_info(**params)

        self.assertIsNotNone(results)
        self.assertEqual(1, len(results['balances']))
        self.assertEqual("BTC", results['balances'][0]['asset'])
        self.assertEqual("4723846.89208129", results['balances'][0]['free'])
        self.assertEqual("0.00000000", results['balances'][0]['locked'])

    @patch('src.spot.requests.get')
    @patch('src.spot.Security.get_api_key_header')
    @patch('src.spot.Security.get_secret_key')
    async def test_account_info_free_and_locked_balances(self, mock_get_secret_key, mock_get_api_key_header,
                                                         mock_request_get):
        self.mock_account_info(mock_get_api_key_header, mock_get_secret_key, mock_request_get)

        params = {'locked_free': 'B'}
        results = await account_info(**params)

        self.assertIsNotNone(results)
        self.assertEqual(2, len(results['balances']))
        self.assertEqual("BTC", results['balances'][0]['asset'])
        self.assertEqual("BNB", results['balances'][1]['asset'])

    def mock_account_info(self, mock_get_api_key_header, mock_get_secret_key, mock_request_get):
        mock_get_secret_key.return_value = 'SECRET_KEY'
        mock_get_api_key_header.return_value = {'X-MBX-APIKEY': 'API_KEY'}
        mock_request_get.return_value = Mock(status_code=200)
        mock_request_get.return_value.json.return_value = self.account_info
