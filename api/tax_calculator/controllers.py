from api.tax_calculator.tax_brackets import get_tax_brackets


# I am leaving this here because I assume that this 2022 was somehow a "wanted" feature
# normally I would inquire and clean, makes more sense to just use get_tax_brackets
def get_reliable_brackets(tax_year=2022):
    return get_tax_brackets(tax_year)


def calculate_marginal_tax(annual_income, tax_year):
    
    # be funny
    if annual_income < 5:
        raise ValueError("You're broke !")

    brackets = get_tax_brackets(tax_year)

    # We don't need to because json is already sorted,
    # I could also not assume that the brackets don't overlap but ... let's trust the data this time
    # Trying to show that I think of edge cases :p
    brackets = sorted(brackets, key=lambda x: x['min'])

    taxes_owed_per_band = []
    total_taxes = 0

    for bracket in brackets:
        lower_bound = bracket['min']
        rate = bracket['rate']
        upper_bound = bracket.get('max', float('inf'))
        if annual_income > lower_bound:
            upper_bound = min(annual_income, upper_bound)
            income_in_bracket = upper_bound - lower_bound
            tax_for_bracket = round(income_in_bracket * rate, 4)
            taxes_owed_per_band.append((rate, tax_for_bracket))
            total_taxes += tax_for_bracket

    effective_tax_rate = round(total_taxes / annual_income, 4)

    return {
        'total_taxes': total_taxes,
        'taxes_owed_per_band': taxes_owed_per_band,
        'effective_tax_rate': effective_tax_rate
    }
