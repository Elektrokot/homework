import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions


def test_load_transactions_success() -> None:
    """Тестирует успешную загрузку транзакций из JSON-файла."""
    test_data = [{"id": 1, "amount": 100.0, "date": "2023-01-01"}, {"id": 2, "amount": 200.0, "date": "2023-01-02"}]
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=json.dumps(test_data))),
    ):
        result = load_transactions("test.json")

        assert isinstance(result, list)
        assert len(result) == 2
        assert result == test_data


def test_load_transactions_file_not_found() -> None:
    """Тестирует случай, когда файл не существует."""
    with patch("os.path.exists", return_value=False):
        result = load_transactions("nonexistent.json")

        assert isinstance(result, list)
        assert len(result) == 0


def test_load_transactions_invalid_file_type() -> None:
    """Тестирует выброс TypeError при неверном типе file_path."""
    with pytest.raises(TypeError, match="file_path должен быть строкой"):
        load_transactions(123)  # type: ignore[arg-type]


def test_load_transactions_json_decode_error() -> None:
    """Тестирует обработку JSONDecodeError при некорректном JSON."""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data="invalid json")),
        patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "invalid json", 0)),
    ):
        result = load_transactions("test.json")

        assert isinstance(result, list)
        assert len(result) == 0


def test_load_transactions_non_list_data() -> None:
    """Тестирует случай, когда данные в файле не являются списком."""
    test_data = {"key": "value"}
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=json.dumps(test_data))),
    ):
        result = load_transactions("test.json")

        assert isinstance(result, list)
        assert len(result) == 0


def test_load_transactions_file_not_found_error() -> None:
    """Тестирует обработку FileNotFoundError."""
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", side_effect=FileNotFoundError("File not found")),
    ):
        result = load_transactions("test.json")

        assert isinstance(result, list)
        assert len(result) == 0


def test_load_transactions_unexpected_error() -> None:
    """Тестирует обработку неожиданной ошибки."""
    with patch("os.path.exists", return_value=True), patch("builtins.open", side_effect=Exception("Unexpected error")):
        result = load_transactions("test.json")

        assert isinstance(result, list)
        assert len(result) == 0
