import pytest
from click import BadParameter

from src.validation.val_cli import validate_output_value


@pytest.mark.parametrize("values", ['JSONN', 'YAMLL', 'aml', 'tables', 't', 'y', 'j'])
def test_validate_output_value_incorrect_value(values):
    with pytest.raises(BadParameter, match=f'{values}. Possible values: json | table | yaml'):
        validate_output_value(None, None, values)


@pytest.mark.parametrize("values", ['json', 'table', 'yaml'])
def test_validate_output_value_correct_value(values):
    assert validate_output_value(None, None, values) == values
