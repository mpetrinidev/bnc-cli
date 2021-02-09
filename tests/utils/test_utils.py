from unittest import TestCase

from src.utils.utils import Utils


class TestUtils(TestCase):
    def setUp(self) -> None:
        pass


class TestInit(TestUtils):
    def test_to_query_string_parameters_empty_values(self):
        values = {}
        self.assertRaises(ValueError, Utils.to_query_string_parameters, values)

    def test_to_query_string_parameters_empty_values_ex_message(self):
        values = {}
        self.assertRaisesRegex(ValueError, 'values cannot be empty', Utils.to_query_string_parameters, values)

    def test_to_query_string_parameters_is_empty_str(self):
        dic = {'test': 'test'}
        self.assertEqual(Utils.to_query_string_parameters(dic), "test=test")
