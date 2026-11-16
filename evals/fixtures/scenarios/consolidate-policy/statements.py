def statement_shipping(subtotal_cents):
    if subtotal_cents < 0:
        raise ValueError('negative subtotal')
    return 0 if subtotal_cents >= 5000 else 500
