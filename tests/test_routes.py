import pytest

from api.error_handlers import format_error
from api.tax_calculator.tax_brackets import get_tax_brackets


# I would split these into one class per route url as well
@pytest.fixture
def supported_years():
    return ['2019', '2020', '2021', '2022', '2023']


def test_tax_calculator_missing_annual_income(client):
    resp = client.get('/tax-calculator/')
    assert resp.status_code == 400
    assert resp.json == {
        'errors': [{
            'field': 'annual_income',
            'message': 'Please provide annual income',
            'code': 'NO_ANNUAL_INCOME'
        }]
    }


def test_tax_calculator_missing_tax_year(client):
    resp = client.get('/tax-calculator/', query_string={'annual_income': '50000'})
    assert resp.status_code == 400
    assert resp.json == {
        'errors': [{
            'field': 'tax_year',
            'message': 'Please provide tax year',
            'code': 'NO_TAX_YEAR'
        }]
    }


def test_tax_calculator_bad_annual_income_type(client):
    resp = client.get('/tax-calculator/', query_string={'annual_income': 'not a number', 'tax_year': 2021})
    assert resp.status_code == 400
    assert resp.json == {
        'errors': [{
            'field': 'annual_income',
            'message': 'Annual_income must be a number',
            'code': 'INVALID_ANNUAL_INCOME'
        }]
    }


def test_tax_calculator_bad_tax_year(client):
    resp = client.get('/tax-calculator/', query_string={'annual_income': '50000', 'tax_year': '2021.45'})
    assert resp.status_code == 400
    assert resp.json == {
        'errors': [{
            'field': 'tax_year',
            'message': 'tax_year must be a valid year',
            'code': 'INVALID_TAX_YEAR'
        }]
    }


def test_tax_calculator_year_not_supported(client):
    resp = client.get('/tax-calculator/', query_string={'annual_income': '50000', 'tax_year': '2025'})
    assert resp.status_code == 400
    assert resp.json == {
        'errors': [{
            'field': 'tax_year',
            'message': 'tax_year must be between 2019 and 2023 inclusively',
            'code': 'TAX_YEAR_OUT_OF_RANGE'
        }]
    }


def test_tax_calculator_success(client):
    resp = client.get('/tax-calculator/', query_string={'annual_income': '50000', 'tax_year': '2020'})
    assert resp.status_code == 200
    assert resp.json == {'effective_tax_rate': 0.1516,
                         'taxes_owed_per_band': [[0.15, 7280.25], [0.205, 300.325]],
                         'total_taxes': 7580.575}


def test_tax_calculator_other_errors(client):
    resp = client.get('/tax-calculator/', query_string={'annual_income': '4', 'tax_year': '2020'})
    assert resp.status_code == 520
    assert resp.json == {'errors': [{'code': '', 'field': '', 'message': "You're broke !"}]}


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
        field="tax_year",
        code="UNSUPPORTED_YEAR"
    )

    unsupported_year = '9999'
    resp = client.get(f'/tax-calculator/tax-brackets/{unsupported_year}')
    data = resp.json
    assert data['errors'] == expected_result_data
