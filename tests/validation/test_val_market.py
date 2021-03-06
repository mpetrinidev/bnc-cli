import pytest
from click import BadParameter

from bnc.validation.val_market import validate_interval


@pytest.mark.parametrize("value", ['seconds', 'minutes', 'days', 'sec', 'min', 'd'])
def test_validate_interval_incorrect_value(value):
    with pytest.raises(BadParameter, match=f'{value}. Possible values: 1m | 3m | 5m | 15m | 30m | 1h | 2h | 4h | 6h | '
                                           f'8h | 12h '
                                           f'| 1d | 3d | 1w | 1M'):
        validate_interval(None, None, value)


@pytest.mark.parametrize("value", ["1m", "3m", "5m", "15m", "30m", "1h",
                                   "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"])
def test_validate_interval_correct_value(value):
    assert validate_interval(None, None, value) == value
