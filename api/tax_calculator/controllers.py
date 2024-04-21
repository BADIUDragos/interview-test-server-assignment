from .tax_brackets import get_tax_brackets


def get_reliable_brackets(tax_year='2022'):
    return get_tax_brackets(tax_year)


