import json
import unittest

import pytest
from unittest.mock import mock_open, patch
from api.tax_calculator.tax_brackets import get_tax_brackets


class TestGetTaxBrackets:

    @pytest.fixture(scope="class")
    def test_data(self):
        self.expected_data = [
            {"min": 0, "max": 47630, "rate": 0.15},
            {"min": 47630, "max": 95259, "rate": 0.205}
        ]
        self.bad_year = 9999
        self.good_year = 2019
        return self

    def test_get_tax_brackets_success(self, test_data):

        mocked_file_content = json.dumps(test_data.expected_data)

        with patch('builtins.open', mock_open(read_data=mocked_file_content)):
            result = get_tax_brackets(test_data.good_year)

            assert result == test_data.expected_data

    def test_get_tax_brackets_error_raised(self, test_data):
        with pytest.raises(ValueError) as exc_info:
            get_tax_brackets(test_data.bad_year)
        assert "does not exist" in str(exc_info.value)


