import pytest
from generators import filter_by_currency

def test_filter_by_currency_raises_value_error_on_invalid_currency(sample_transactions):
    with pytest.raises(ValueError):
        list(filter_by_currency(sample_transactions, "INVALID_CURRENCY"))