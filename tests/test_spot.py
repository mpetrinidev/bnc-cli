from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from src.spot import Spot


class TestSpot(TestCase):
    def setUp(self) -> None:
        self.spot = Spot()

    def test_validate_account_info_recv_window_greater_than_60000(self):
        params = {'recv_window': 60_001}
        self.assertRaisesRegex(ValueError, 'recv_window cannot exceed 60_000', self.spot.validate_account_info, params)

    def test_validate_account_info_recv_window_is_str_and_greater_than_60000(self):
        params = {'recv_window': '60_001'}
        self.assertRaisesRegex(ValueError, 'recv_window cannot exceed 60_000', self.spot.validate_account_info, params)

    def test_validate_account_info_locked_free_incorrect_value(self):
        params = {'locked_free': 'G'}
        self.assertRaisesRegex(ValueError, 'locked_free incorrect value. Possible values: L | F | B',
                               self.spot.validate_account_info, params)


class TestSpotAsync(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.spot = Spot()

    @patch('src.spot.requests.get')
    @patch('src.spot.Security.get_api_key_header')
    @patch('src.spot.Security.get_secret_key')
    async def test_account_info_return_ok(self, mock_get_secret_key, mock_get_api_key_header, mock_request_get):
        mock_get_secret_key.return_value = 'SECRET_KEY'
        mock_get_api_key_header.return_value = {'X-MBX-APIKEY': 'API_KEY'}

        spot_info = {
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
                }
            ]
        }

        mock_request_get.return_value = Mock(status_code=200)
        mock_request_get.return_value.json.return_value = spot_info

        params = {'recv_window': 5000}
        results = await self.spot.account_info(**params)

        self.assertIsNotNone(results)
        self.assertEqual(15, results["makerCommission"])


