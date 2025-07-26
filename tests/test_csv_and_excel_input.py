import os
from unittest.mock import MagicMock, Mock, mock_open, patch

import pandas as pd
import pytest

from src.csv_and_excel_input import read_csv_transactions, read_excel_transactions

# === Фикстуры ===


@pytest.fixture
def valid_csv_data():  # type: ignore[no-untyped-def]
    return (
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;"
        "Счет 39745660563456619397;Перевод организации"
    )


@pytest.fixture
def valid_excel_data():  # type: ignore[no-untyped-def]
    """Корректные данные для Excel (в виде списка словарей)."""
    return [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]


@pytest.fixture
def invalid_file_path():  # type: ignore[no-untyped-def]
    """Несуществующий путь к файлу."""
    return "invalid/path/transactions.csv"


@pytest.fixture
def mock_pandas_dataframe():  # type: ignore[no-untyped-def]
    """Создает мок для DataFrame с тестовыми данными."""
    df = Mock()
    df.to_dict.return_value = [
        {"id": 1, "amount": 100.0, "date": "2023-01-01"},
        {"id": 2, "amount": 200.0, "date": "2023-01-02"},
    ]
    return df


# === Тесты для read_csv_transactions ===


@patch("os.path.exists", return_value=True)
@patch("builtins.open")
def test_read_csv_success(mock_file, valid_csv_data):  # type: ignore[no-untyped-def]
    """Тест успешного чтения корректного CSV."""
    # Настраиваем open() через __enter__
    mock_file.return_value.__enter__.return_value.read.return_value = valid_csv_data

    # Мокаем DictReader
    with patch("csv.DictReader") as mock_reader:
        mock_reader.return_value = [{"id": "650703", "amount": "16210"}]

        result = read_csv_transactions("input_data/transactions.csv")

    assert len(result) == 1
    assert result[0]["id"] == "650703"


@patch("os.path.exists", return_value=True)
@patch("builtins.open", side_effect=FileNotFoundError("Файл не найден"))
def test_read_csv_file_not_found(mock_file, mock_exists):  # type: ignore[no-untyped-def]
    """Тест: файл CSV не найден."""
    result = read_csv_transactions("input_data/missing.csv")
    assert result == []


@patch("os.path.exists", return_value=True)
@patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid encoding"))
def test_read_csv_decode_error(mock_file, mock_exists):  # type: ignore[no-untyped-def]
    """Тест: ошибка кодировки CSV."""
    result = read_csv_transactions("input_data/bad_encoding.csv")
    assert result == []


@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data="")
def test_read_csv_empty_file(mock_file, mock_exists):  # type: ignore[no-untyped-def]
    """Тест: пустой CSV-файл."""
    result = read_csv_transactions("input_data/empty.csv")
    assert result == []


# Параметризованные тесты для read_csv_transactions
@pytest.mark.parametrize(
    "file_path, file_content, expected_result",
    [
        (
            "input_data/valid.csv",
            "id;amount\n1;100",
            [
                {
                    "id": "1",
                    "state": None,
                    "date": None,
                    "description": None,
                    "from": None,
                    "to": None,
                    "operationAmount": {"amount": "100", "currency": {"name": "руб.", "code": "RUB"}},
                }
            ],
        ),
        ("input_data/empty.csv", "", []),
        ("invalid/path.csv", None, []),
    ],
)
def test_read_csv_variants(file_path, file_content, expected_result, tmpdir):  # type: ignore[no-untyped-def]
    """Параметризованный тест для различных сценариев чтения CSV."""
    if file_content:
        mock_file = tmpdir.join("test.csv")
        mock_file.write(file_content)
        with patch("os.path.exists", return_value=os.path.exists(mock_file.strpath)):
            result = read_csv_transactions(mock_file.strpath)
    else:
        result = read_csv_transactions(file_path)
    assert result == expected_result


# === Тесты для read_excel_transactions ===


def test_read_excel_transactions_success() -> None:
    """Тестирует успешное чтение Excel-файла."""
    # Создаем мок данные, которые будут имитировать DataFrame
    mock_data = [{"id": "1", "amount": "100"}, {"id": "2", "amount": "200"}]

    # Создаем мок объект DataFrame
    mock_pandas_dataframe = MagicMock()
    mock_pandas_dataframe.iterrows.return_value = enumerate(mock_data)  # Имитация iterrows()

    # Патчим os.path.exists и pandas.read_excel
    with patch("os.path.exists", return_value=True), patch("pandas.read_excel", return_value=mock_pandas_dataframe):
        result = read_excel_transactions("test.xlsx")

    # Ожидаемый результат с полной структурой данных
    expected_result = [
        {
            "id": "1",
            "state": None,
            "date": None,
            "description": None,
            "from": None,
            "to": None,
            "operationAmount": {"amount": "100", "currency": {"name": "руб.", "code": "RUB"}},
        },
        {
            "id": "2",
            "state": None,
            "date": None,
            "description": None,
            "from": None,
            "to": None,
            "operationAmount": {"amount": "200", "currency": {"name": "руб.", "code": "RUB"}},
        },
    ]

    # Проверяем результат
    assert result == expected_result


def test_read_excel_transactions_file_not_found():  # type: ignore[no-untyped-def]
    """Тестирует случай, когда файл не существует."""
    with patch("os.path.exists", return_value=False):
        result = read_excel_transactions("nonexistent.xlsx")

        assert isinstance(result, list)
        assert len(result) == 0
        assert result == []


def test_read_excel_transactions_invalid_file_type():  # type: ignore[no-untyped-def]
    """Тестирует выброс TypeError при неверном типе file_path."""
    with pytest.raises(TypeError, match="file_path должен быть строкой."):
        read_excel_transactions(123)  # type: ignore[arg-type]


def test_read_excel_transactions_parser_error(mock_pandas_dataframe):  # type: ignore[no-untyped-def]
    """Тестирует обработку ParserError при чтении файла."""
    with (
        patch("os.path.exists", return_value=True),
        patch("pandas.read_excel", side_effect=pd.errors.ParserError("Invalid file format")),
    ):
        result = read_excel_transactions("test.xlsx")

        assert isinstance(result, list)
        assert len(result) == 0


def test_read_excel_transactions_unicode_decode_error(mock_pandas_dataframe):  # type: ignore[no-untyped-def]
    """Тестирует обработку UnicodeDecodeError при чтении файла."""
    with (
        patch("os.path.exists", return_value=True),
        patch("pandas.read_excel", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")),
    ):
        result = read_excel_transactions("test.xlsx")

        assert isinstance(result, list)
        assert len(result) == 0


def test_read_excel_transactions_file_not_found_error(mock_pandas_dataframe):  # type: ignore[no-untyped-def]
    """Тестирует обработку FileNotFoundError при чтении файла."""
    with (
        patch("os.path.exists", return_value=True),
        patch("pandas.read_excel", side_effect=FileNotFoundError("File not found")),
    ):
        result = read_excel_transactions("test.xlsx")

        assert isinstance(result, list)
        assert len(result) == 0
