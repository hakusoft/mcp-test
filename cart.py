"""Shopping cart price calculation."""


def calculate_total(items, tax_rate=0.1):
    """Return the tax-included total for a list of cart items.

    Each item is a dict with "price" and "quantity".
    """
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["quantity"]
    return subtotal * (1 + tax_rate)


def apply_discount(total, rate):
    """Apply a discount rate (0.0-1.0) to a total."""
    return total * (1 - rate)
