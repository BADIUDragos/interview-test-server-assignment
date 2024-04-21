import json

import pytest
from unittest.mock import mock_open, patch

from api.tax_calculator.controllers import get_reliable_brackets
from tests.test_tax_brackets import TestGetTaxBrackets


class TestGetReliableBrackets(TestGetTaxBrackets):

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


