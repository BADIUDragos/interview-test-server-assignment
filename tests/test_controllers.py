import json

import pytest
from unittest.mock import mock_open, patch

from api.tax_calculator.controllers import get_reliable_brackets, calculate_marginal_tax
from tests.test_tax_brackets import TestData


# Maybe not the best way of doing this
class TestGetReliableBrackets(TestData):

    def test_get_reliable_brackets_success(self, test_data):
        mocked_file_content = json.dumps(test_data.expected_data)

        with patch('builtins.open', mock_open(read_data=mocked_file_content)):
            result = get_reliable_brackets(test_data.good_year)

            assert result == test_data.expected_data

    def test_get_reliable_brackets_default_2022(self):
        expected_data = [
            {"min": 0, "max": 47630, "rate": 0.15},
            {"min": 50000, "max": 95259, "rate": 0.205}
        ]

        mocked_file_content = json.dumps(expected_data)

        with patch('builtins.open', mock_open(read_data=mocked_file_content)):
            result = get_reliable_brackets(2022)

            assert result == expected_data

    def test_get_reliable_brackets_error_raised(self, test_data):
        with pytest.raises(ValueError) as exc_info:
            get_reliable_brackets(test_data.bad_year)
        assert "does not exist" in str(exc_info.value)


class TestCalculateMarginalTax:

    @pytest.fixture(scope='class')
    def test_data(self):
        self.mock_brackets = [
            {"min": 0, "max": 20000, "rate": 0.0},
            {"min": 20000, "max": 40000, "rate": 0.1},
            {"min": 40000, "max": 60000, "rate": 0.2},
            {"min": 60000, "max": 80000, "rate": 0.3},
            {"min": 80000, "rate": 0.4}
        ]

        self.expected_result_first_band_income = {'effective_tax_rate': 0.0,
                                                  'taxes_owed_per_band': [(0.0, 0.0)],
                                                  'total_taxes': 0.0}

        self.expected_result_30000_income = {'effective_tax_rate': 0.0333,
                                             'taxes_owed_per_band': [(0.0, 0.0), (0.1, 1000.0)],
                                             'total_taxes': 1000.0}

        self.expected_result_float_income = {'effective_tax_rate': 0.0333,
                                             'taxes_owed_per_band': [(0.0, 0.0), (0.1, 1000.045)],
                                             'total_taxes': 1000.045}

        self.expected_result_last_band_income = {'effective_tax_rate': 0.2,
                                                 'taxes_owed_per_band': [(0.0, 0.0),
                                                                         (0.1, 2000.0),
                                                                         (0.2, 4000.0),
                                                                         (0.3, 6000.0),
                                                                         (0.4, 8000.0)],
                                                 'total_taxes': 20000.0}

        return self

    def test_broke(self):
        with pytest.raises(ValueError) as e:
            calculate_marginal_tax(4, 2020)
        assert "You're broke !" == str(e.value)

    def test_calculate_marginal_tax_single_band(self, test_data):
        with patch('api.tax_calculator.controllers.get_tax_brackets', return_value=test_data.mock_brackets):
            result = calculate_marginal_tax(15000, 2020)
            assert result == test_data.expected_result_first_band_income

    def test_calculate_marginal_tax_income_equals_bracket_upper_bound(self, test_data):
        with patch('api.tax_calculator.controllers.get_tax_brackets', return_value=test_data.mock_brackets):
            result = calculate_marginal_tax(20000, 2020)
            assert result == test_data.expected_result_first_band_income

    def test_calculate_marginal_tax_income_middle_second_band(self, test_data):
        with patch('api.tax_calculator.controllers.get_tax_brackets', return_value=test_data.mock_brackets):
            result = calculate_marginal_tax(30000, 2020)
            assert result == test_data.expected_result_30000_income

    def test_calculate_marginal_tax_income_float(self, test_data):
        with patch('api.tax_calculator.controllers.get_tax_brackets', return_value=test_data.mock_brackets):
            result = calculate_marginal_tax(30000.45, 2020)
            assert result == test_data.expected_result_float_income

    def test_calculate_marginal_tax_income_no_max_band(self, test_data):
        with patch('api.tax_calculator.controllers.get_tax_brackets', return_value=test_data.mock_brackets):
            result = calculate_marginal_tax(100000, 2020)
            assert result == test_data.expected_result_last_band_income
