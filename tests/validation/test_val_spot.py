import pytest
from click import BadParameter

from bnc.validation.val_spot import validate_recv_window, validate_side, validate_time_in_force, \
    validate_new_order_resp_type


@pytest.mark.parametrize("value", [60001, '60001'])
def test_validate_recv_window_greater_than_60000(value):
    with pytest.raises(BadParameter, match=f'{value}. Cannot exceed 60000'):
        validate_recv_window(None, None, value)


@pytest.mark.parametrize("value", [60000, '60000', 5000, '5000', 1000, '1000'])
def test_validate_recv_window_correct_value(value):
    assert validate_recv_window(None, None, value) == value


@pytest.mark.parametrize("value", ['B', 'BUYY', 'S', 'SELLL', ''])
def test_validate_side_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: BUY | SELL'):
        validate_side(None, None, value)


@pytest.mark.parametrize("value", ['BUY', 'SELL'])
def test_validate_side_correct_value(value):
    assert validate_side(None, None, value) == value


def test_validate_time_in_force_null_value():
    assert validate_time_in_force(None, None, None) is None


@pytest.mark.parametrize("value", ['GTCC', 'G', 'IOV', 'F0K', 'I0C'])
def test_validate_time_in_force_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: GTC | IOC | FOK'):
        validate_time_in_force(None, None, value)


@pytest.mark.parametrize("value", ['GTC', 'IOC', 'FOK'])
def test_validate_time_in_force_correct_value(value):
    assert validate_time_in_force(None, None, value) == value


@pytest.mark.parametrize("value", ['ACKK', 'FULLL', 'RESULTS', 'TEST', 'R'])
def test_validate_new_order_resp_type_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: FULL | ACK | RESULT'):
        validate_new_order_resp_type(None, None, value)


@pytest.mark.parametrize("value", ['ACK', 'FULL', 'RESULT'])
def test_validate_new_order_resp_type_correct_value(value):
    assert validate_new_order_resp_type(None, None, value) == value
