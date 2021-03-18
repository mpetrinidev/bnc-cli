import pytest
from click import BadParameter

from src.validation.val_spot import validate_recv_window, validate_locked_free, validate_side, validate_time_in_force, \
    validate_new_order_resp_type


def test_validate_recv_window_is_none():
    with pytest.raises(BadParameter, match='recv_window cannot be null'):
        validate_recv_window(None, None, None)


@pytest.mark.parametrize("value", [60001, '60001'])
def test_validate_recv_window_greater_than_60000(value):
    with pytest.raises(BadParameter, match=f'{value}. Cannot exceed 60000'):
        validate_recv_window(None, None, value)


@pytest.mark.parametrize("value", ['G', 'LL', 'FF', 'BB', 2])
def test_validate_locked_free_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: A | L | F | B'):
        validate_locked_free(None, None, value)


@pytest.mark.parametrize("value", ['B', 'BUYY', 'S', 'SELLL', ''])
def test_validate_side_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: BUY | SELL'):
        validate_side(None, None, value)


@pytest.mark.parametrize("value", ['GTCC', 'G', 'IOV', 'F0K', 'I0C'])
def test_validate_time_in_force_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: GTC | IOC | FOK'):
        validate_time_in_force(None, None, value)


@pytest.mark.parametrize("value", ['ACKK', 'FULLL', 'RESULTS', 'TEST', 'R'])
def test_validate_new_order_resp_type_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: FULL | ACK | RESULT'):
        validate_new_order_resp_type(None, None, value)
