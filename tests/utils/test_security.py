from unittest import TestCase

from src.utils.security import Security


class TestSecurity(TestCase):
    def setUp(self) -> None:
        pass


class TestInit(TestSecurity):
    def test_get_hmac_hash_total_params_is_empty_string(self):
        self.assertRaisesRegex(ValueError, 'total_params cannot be empty', Security.get_hmac_hash, '', 'secret')

    def test_get_hmac_hash_secret_is_empty_string(self):
        self.assertRaisesRegex(ValueError, 'secret cannot be empty', Security.get_hmac_hash, 'total_params', '')

    def test_get_hmac_hash_secret_new_signature(self):
        total_params = "hello_world"
        secret = 'SECRET_KEY_EXAMPLE'

        self.assertEqual(Security.get_hmac_hash(total_params, secret),
                         '32d322a281bcd36c64af2bc97e13eee974f24ac900fe4dc7b4901f166d72e6cc')
