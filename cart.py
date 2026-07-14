"""Shopping cart price calculation."""


def calculate_total(items, tax_rate=0.1):
    """Return the tax-included total for a list of cart items.

    Each item is a dict with "price" and "quantity".
    The result is rounded to 2 decimal places, since binary floats
    cannot represent tax rates like 0.1 exactly.
    """
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["quantity"]
    return round(subtotal * (1 + tax_rate), 2)


def apply_discount(total, rate):
    """Apply a discount rate to a total.

    Raises:
        ValueError: if rate is outside the 0.0-1.0 range.
    """
    if not 0.0 <= rate <= 1.0:
        raise ValueError(f"rate must be between 0.0 and 1.0, got {rate}")
    return total * (1 - rate)
