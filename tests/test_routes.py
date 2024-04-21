import pytest

from api.error_handlers import format_error
from api.tax_calculator.tax_brackets import get_tax_brackets


@pytest.fixture
def supported_years():
    return ['2019', '2020', '2021', '2022', '2023']


def test_tax_calculator_instructions(client):
    resp = client.get('/tax-calculator/')
    brackets = get_tax_brackets(2022)
    assert resp.json == {'tax_brackets': brackets}


def test_default_brackets(client):
    resp = client.get('/tax-calculator/tax-year')
    assert resp.status_code == 302
    assert resp.headers['Location'] == '/'


def test_tax_year_brackets(client, supported_years):

    for year in supported_years:
        resp = client.get(f'/tax-calculator/tax-brackets/{year}')
        brackets = get_tax_brackets(year)
        data = resp.json
        assert data['tax_brackets'] == brackets


def test_tax_year_brackets_unsupported_year(client, supported_years):
    expected_result_data = format_error(
            message="We only support tax calculations for years: " + ", ".join(supported_years),
            field="tax year",
            code="UNSUPPORTED_YEAR"
        )

    unsupported_year = '9999'
    resp = client.get(f'/tax-calculator/tax-brackets/{unsupported_year}')
    data = resp.json
    assert data['errors'] == expected_result_data
