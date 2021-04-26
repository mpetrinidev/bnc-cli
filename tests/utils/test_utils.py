import pytest

from bnc.utils.utils import to_query_string_parameters


def test_to_query_string_parameters_empty_values():
    values = {}
    with pytest.raises(ValueError, match='values cannot be empty'):
        to_query_string_parameters(values)


def test_to_query_string_parameters_is_empty_str():
    dic = {'test': 'test'}
    assert to_query_string_parameters(dic) == "test=test"
