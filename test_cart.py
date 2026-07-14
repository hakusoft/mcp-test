import pytest

import cart


def test_calculate_total():
    items = [{"price": 100, "quantity": 2}]
    assert cart.calculate_total(items) == 220.0


def test_calculate_total_empty():
    assert cart.calculate_total([]) == 0


def test_apply_discount():
    assert cart.apply_discount(1000, 0.2) == 800.0


@pytest.mark.parametrize("rate", [1.5, -0.2])
def test_apply_discount_rejects_invalid_rate(rate):
    with pytest.raises(ValueError):
        cart.apply_discount(1000, rate)


@pytest.mark.parametrize("rate,expected", [(0.0, 1000.0), (1.0, 0.0)])
def test_apply_discount_accepts_bounds(rate, expected):
    assert cart.apply_discount(1000, rate) == expected
