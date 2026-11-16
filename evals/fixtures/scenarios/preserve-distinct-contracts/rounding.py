from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP

def invoice_amount(value):
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def payroll_amount(value):
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
