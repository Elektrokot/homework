import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transactions


class TestUtils(unittest.TestCase):

    @patch("os.path.exists", return_value=False)
    def test_file_not_found_returns_empty_list(self, mock_exists):  # type: ignore[no-untyped-def]
        result = load_transactions("nonexistent.json")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_invalid_json_returns_empty_list(self, mock_file, mock_exists):  # type: ignore[no-untyped-def]
        result = load_transactions("data/operations.json")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_empty_list_returns_empty_list(self, mock_file, mock_exists):  # type: ignore[no-untyped-def]
        result = load_transactions("data/operations.json")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}]')
    def test_valid_json_list_returns_list(self, mock_file, mock_exists):  # type: ignore[no-untyped-def]
        result = load_transactions("data/operations.json")
        self.assertEqual(result, [{"id": 1}])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_non_list_json_returns_empty_list(self, mock_file, mock_exists):  # type: ignore[no-untyped-def]
        result = load_transactions("data/operations.json")
        self.assertEqual(result, [])
