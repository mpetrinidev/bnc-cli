from unittest import TestCase

from src.utils.security import Security


class TestSecurity(TestCase):
    def setUp(self) -> None:
        pass


API_KEY = 'SET_YOUR_API_KEY'
SECRET_KEY = 'SET_YOUR_SECRET_KEY'


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

    def test_set_api_key_is_empty(self):
        api_key = ''
        self.assertRaisesRegex(ValueError, 'api_key cannot be empty', Security.set_api_key, api_key)

    def test_set_api_key_is_ok(self):
        Security.set_api_key(API_KEY)

        self.assertEqual(API_KEY, Security.get_api_key())
        Security.del_api_key()

    def test_get_api_key_raises_exception(self):
        Security.del_api_key()
        self.assertRaisesRegex(ValueError, 'You must set bnc api_key to start using the CLI', Security.get_api_key)

    def test_get_api_key_is_ok(self):
        Security.set_api_key(API_KEY)

        self.assertEqual(API_KEY, Security.get_api_key())

        Security.del_api_key()

    def test_get_api_key_header_raises_exception(self):
        Security.del_api_key()
        self.assertRaisesRegex(ValueError, 'You must set bnc api_key to start using the CLI',
                               Security.get_api_key_header)

    def test_get_api_key_header_is_ok(self):
        expected_dic = {'X-MBX-APIKEY': API_KEY}
        Security.set_api_key(API_KEY)

        self.assertDictEqual(Security.get_api_key_header(), expected_dic)

        Security.del_api_key()

    def test_set_secret_key_is_empty(self):
        secret_key = ''
        self.assertRaisesRegex(ValueError, 'secret_key cannot be empty', Security.set_secret_key, secret_key)

    def test_set_secret_key_is_ok(self):
        Security.set_secret_key(SECRET_KEY)

        self.assertEqual(SECRET_KEY, Security.get_secret_key())
        Security.del_secret_key()

    def test_get_secret_key_raises_exception(self):
        Security.del_secret_key()
        self.assertRaisesRegex(ValueError, 'You must set bnc secret_key to start using the CLI', Security.get_secret_key)

    def test_get_secret_key_is_ok(self):
        Security.set_secret_key(SECRET_KEY)

        self.assertEqual(SECRET_KEY, Security.get_secret_key())

        Security.del_secret_key()
