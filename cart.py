"""Shopping cart price calculation."""


def calculate_total(
    items,
    tax_rate=0.1,
    shipping_fee=0,
    free_shipping_threshold=5000,
):
    """Return the tax-included total for a list of cart items.

    Each item is a dict with "price" and "quantity".
    `shipping_fee` is added to the subtotal before tax, unless the
    (pre-tax) subtotal already meets `free_shipping_threshold`, in which
    case shipping is free. Defaults to 0 so callers who don't pass
    `shipping_fee` see no change in behavior.
    The result is rounded to 2 decimal places, since binary floats
    cannot represent tax rates like 0.1 exactly.
    """
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["quantity"]
    if subtotal < free_shipping_threshold:
        subtotal += shipping_fee
    return round(subtotal * (1 + tax_rate), 2)


def apply_discount(total, rate):
    """Apply a discount rate to a total.

    Raises:
        ValueError: if rate is outside the 0.0-1.0 range.
    """
    if not 0.0 <= rate <= 1.0:
        raise ValueError(f"rate must be between 0.0 and 1.0, got {rate}")
    return total * (1 - rate)
