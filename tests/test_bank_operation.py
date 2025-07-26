from typing import Dict, List

import pytest

from src.bank_operation import process_bank_operations, process_bank_search


# Тестовые данные
@pytest.mark.parametrize(
    "data, search, expected",
    [
        # Позитивный тест
        (
            [
                {"description": "Payment for groceries", "amount": 100},
                {"description": "Groceries at store", "amount": 50},
            ],
            "groceries",
            [
                {"description": "Payment for groceries", "amount": 100},
                {"description": "Groceries at store", "amount": 50},
            ],
        ),
        # Регистронезависимость
        (
            [{"description": "Payment for Groceries", "amount": 100}],
            "groceries",
            [{"description": "Payment for Groceries", "amount": 100}],
        ),
        # Пустой список
        ([], "groceries", []),
        # Отсутствие совпадений
        ([{"description": "Payment for rent", "amount": 200}], "groceries", []),
    ],
)
def test_process_bank_search(data: List[Dict], search: str, expected: List[Dict]):  # type: ignore[no-untyped-def]
    result = process_bank_search(data, search)
    assert result == expected


# Тест на некорректные типы данных


def test_process_bank_search_invalid_types() -> None:
    with pytest.raises(TypeError):
        process_bank_search("not a list", "search")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        process_bank_search([], 123)  # type: ignore[arg-type]


# Тестовые данные
@pytest.mark.parametrize(
    "data, categories, expected",
    [
        # Позитивный тест
        (
            [
                {"description": "Payment for groceries", "amount": 100},
                {"description": "Rent payment", "amount": 200},
                {"description": "Groceries at store", "amount": 50},
            ],
            ["groceries", "rent"],
            {"groceries": 2, "rent": 1},
        ),
        # Чувствительность к регистру
        ([{"description": "Payment for Groceries", "amount": 100}], ["groceries"], {"groceries": 1}),
        # Пустой список
        ([], ["groceries", "rent"], {"groceries": 0, "rent": 0}),
        # Отсутствие совпадений
        (
            [{"description": "Payment for utilities", "amount": 150}],
            ["groceries", "rent"],
            {"groceries": 0, "rent": 0},
        ),
    ],
)
def test_process_bank_operations(  # type: ignore[no-untyped-def]
    data: List[Dict], categories: List[str], expected: Dict[str, int]
):
    result = process_bank_operations(data, categories)
    assert result == expected


# Тест на некорректные типы данных


def test_process_bank_operations_invalid_types() -> None:
    with pytest.raises(TypeError):
        process_bank_operations("not a list", ["categories"])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        process_bank_operations([], "not a list")  # type: ignore[arg-type]
