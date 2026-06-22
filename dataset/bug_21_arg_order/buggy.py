def apply_rate(amount, rate):
    """Adjusts `amount` by `rate` percent (positive adds, negative subtracts)."""
    return amount + amount * rate / 100


def net_price(price, discount, tax):
    """Returns the final price: apply the `discount` percent, then add `tax` percent.

    `discount` and `tax` are percentages (e.g. 10 means 10%).
    """
    subtotal = apply_rate(price, -discount)
    return apply_rate(tax, subtotal)
