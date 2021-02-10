from unittest import TestCase

from src.credentials import Credentials
from src.utils.security import Security


class TestCredentials(TestCase):
    def setUp(self) -> None:
        self.credentials = Credentials()

    def test_add_api_key_is_None(self):
        api_key = None
        secret = 'secret'
        self.assertRaisesRegex(ValueError, 'api_key cannot be null or empty', self.credentials.add, api_key, secret)

    def test_add_secret_is_None(self):
        api_key = 'api_key'
        secret = None
        self.assertRaisesRegex(ValueError, 'secret cannot be null or empty', self.credentials.add, api_key, secret)

    def test_add_is_ok(self):
        api_key = 'api_key'
        secret = 'secret'

        self.credentials.add(api_key, secret)

        self.assertEqual(api_key, self.credentials.api_key)
        self.assertEqual(secret, self.credentials.secret)

        self.assertEqual(api_key, Security.get_api_key())
        self.assertEqual(secret, Security.get_secret_key())

        Security.del_api_key()
        Security.del_secret_key()

    def test_remove_is_ok(self):
        self.credentials.remove()

        self.assertRaisesRegex(ValueError, 'You must set bnc api_key to start using the CLI', Security.get_api_key)
        self.assertRaisesRegex(ValueError, 'You must set bnc secret_key to start using the CLI', Security.get_secret_key)

        self.assertIsNone(self.credentials.api_key)
        self.assertIsNone(self.credentials.secret)

