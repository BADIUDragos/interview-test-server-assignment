from api.tax_calculator.tax_brackets import get_tax_brackets


def test_tax_calculator_instructions(client):
    resp = client.get('/tax-calculator/')
    brackets = get_tax_brackets(2022)
    assert resp.json == {'tax_brackets': brackets}


def test_default_brackets(client):
    resp = client.get('/tax-calculator/tax-year')
    assert resp.status_code == 302
    assert resp.headers['Location'] == '/'


def test_tax_year_brackets(client):

    for year in [2019, 2020, 2021, 2022, 2023]:
        resp = client.get(f'/tax-calculator/tax-brackets/{year}')
        brackets = get_tax_brackets(year)
        data = resp.json
        assert data['tax_brackets'] == brackets
