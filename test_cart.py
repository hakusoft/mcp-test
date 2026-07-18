import pytest

import cart


def test_calculate_total():
    items = [{"price": 100, "quantity": 2}]
    assert cart.calculate_total(items) == 220.0


def test_calculate_total_empty():
    assert cart.calculate_total([]) == 0


def test_calculate_total_adds_shipping_fee_below_threshold():
    items = [{"price": 1000, "quantity": 1}]
    assert cart.calculate_total(items, shipping_fee=500) == 1650.0


def test_calculate_total_waives_shipping_fee_at_threshold():
    items = [{"price": 5000, "quantity": 1}]
    assert cart.calculate_total(
        items, shipping_fee=500, free_shipping_threshold=5000
    ) == 5500.0


def test_calculate_total_waives_shipping_fee_above_threshold():
    items = [{"price": 6000, "quantity": 1}]
    assert cart.calculate_total(items, shipping_fee=500) == 6600.0


def test_calculate_total_no_shipping_fee_by_default():
    items = [{"price": 100, "quantity": 2}]
    assert cart.calculate_total(items) == 220.0


@pytest.mark.parametrize("missing_key", ["price", "quantity"])
def test_calculate_total_rejects_item_missing_key(missing_key):
    item = {"price": 100, "quantity": 2}
    del item[missing_key]
    with pytest.raises(ValueError, match=missing_key):
        cart.calculate_total([item])


def test_apply_discount():
    assert cart.apply_discount(1000, 0.2) == 800.0


@pytest.mark.parametrize("rate", [1.5, -0.2])
def test_apply_discount_rejects_invalid_rate(rate):
    with pytest.raises(ValueError):
        cart.apply_discount(1000, rate)


@pytest.mark.parametrize("rate,expected", [(0.0, 1000.0), (1.0, 0.0)])
def test_apply_discount_accepts_bounds(rate, expected):
    assert cart.apply_discount(1000, rate) == expected
