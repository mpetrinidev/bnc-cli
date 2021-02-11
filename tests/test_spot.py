from unittest import TestCase, IsolatedAsyncioTestCase

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

#    async def test_account_info_return_ok(self):
#        params = {'recv_window': 5000}
#        results = await self.spot.account_info(params)
#
#        self.assertIsNotNone(results)
