import cart


def test_calculate_total():
    items = [{"price": 100, "quantity": 2}]
    assert cart.calculate_total(items) == 220.0


def test_calculate_total_empty():
    assert cart.calculate_total([]) == 0


def test_apply_discount():
    assert cart.apply_discount(1000, 0.2) == 800.0
