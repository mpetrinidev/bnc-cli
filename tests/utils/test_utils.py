import pytest

from bnc.utils.utils import to_query_string_parameters, mask_dic_values
from bnc.utils.utils import to_log_str


def test_to_query_string_parameters_empty_values():
    values = {}
    with pytest.raises(ValueError, match='values cannot be empty'):
        to_query_string_parameters(values)


def test_to_query_string_parameters_one_key_pair():
    dic = {'test': 'test'}
    assert to_query_string_parameters(dic) == "test=test"


def test_to_query_string_parameters_multiple_key_pairs():
    dic = {'test': 'test', 'test1': 1, 'test2': True}
    assert to_query_string_parameters(dic) == "test=test&test1=1&test2=True"


def test_to_log_str_empty_dic():
    dic = {}
    with pytest.raises(ValueError, match='dic cannot be empty'):
        to_log_str(dic)


def test_to_log_str_one_key_pair():
    dic = {'test': 'test'}
    assert to_log_str(dic) == "test=test"


def test_to_log_str_multiple_key_pairs():
    dic = {'test': 'test', 'test1': 1, 'test2': True}
    assert to_log_str(dic) == "test=test test1=1 test2=True"


def test_mask_dic_values_dic_empty():
    dic = {}
    with pytest.raises(ValueError, match='dic cannot be empty'):
        mask_dic_values(dic, ['key'])


def test_mask_dic_values_keys_is_none():
    dic = {'key': 'value'}
    keys = None
    with pytest.raises(ValueError, match='keys cannot be null'):
        mask_dic_values(dic, keys)


def test_mask_dic_values_keys_is_empty():
    dic = {'key': 'value'}
    keys = []
    with pytest.raises(ValueError, match='keys cannot be empty'):
        mask_dic_values(dic, keys)


def test_mask_dic_values_change_value():
    dic = {'key': 'secret_value'}
    keys = ['key']

    new_dic = mask_dic_values(dic, keys)

    assert new_dic['key'] == '######'


def test_mask_dic_values_key_not_exists():
    dic = {'key': 'secret_value'}
    keys = ['key1']

    new_dic = mask_dic_values(dic, keys)

    assert new_dic['key'] == 'secret_value'
