def parse_amount(value):
    try:
        return float(str(value).replace('$', '').replace(',', ''))
    except ValueError:
        return None