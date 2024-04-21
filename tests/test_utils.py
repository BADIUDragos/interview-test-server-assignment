import pytest
from unittest.mock import mock_open, patch

from api.utils import _open_fixture


def test_open_config_valid_json():
    file_path = 'tax-brackets--1234.json'
    mock_file_content = '{"key": "value"}'
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        assert _open_fixture(file_path) == {"key": "value"}


def test_open_config_file_not_found():
    file_path = 'nonexistent.json'
    with patch('builtins.open', side_effect=FileNotFoundError):
        with pytest.raises(ValueError) as e:
            _open_fixture(file_path)
        assert str(e.value) == "The file %s does not exist" % file_path


def test_open_config_invalid_json():
    file_path = 'tax-brackets-invalid-content.json'
    mock_file_content = '{"key": "value" some invalid json'
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        with pytest.raises(ValueError) as e:
            _open_fixture(file_path)
        assert "contains invalid JSON" in str(e.value)
