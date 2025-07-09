# from typing import Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.usefixtures("transactions")
def test_filter_by_currency(transactions):  # type: ignore[no-untyped-def]
    """
    Тестируем с валютой USD, которая присутствует в данных.
    """
    usd_transactions = filter_by_currency(transactions, "USD")

    assert next(usd_transactions) == {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }

    assert next(usd_transactions) == {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }

    assert next(usd_transactions) == {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    }

    # Проверяем, что больше транзакций с валютой USD нет
    with pytest.raises(StopIteration):
        next(usd_transactions)


@pytest.mark.usefixtures("transactions")
def test_filter_by_currency_no_matches(transactions):  # type: ignore[no-untyped-def]
    """
    Тест на случай, когда транзакции в заданной валюте отсутствуют.
    """
    rub_transactions = filter_by_currency(transactions, "EUR")

    # Проверяем, что генератор не выдает никаких значений и завершается без ошибок
    with pytest.raises(StopIteration):
        next(rub_transactions)


@pytest.mark.usefixtures("transactions")
def test_filter_by_currency_empty_list(transactions):  # type: ignore[no-untyped-def]
    """
    Тест на случай пустого списка транзакций.
    """
    empty_transactions = []
    empty_rub_transactions = filter_by_currency(empty_transactions, "RUB")

    # Проверяем, что генератор не выдает никаких значений и завершается без ошибок
    with pytest.raises(StopIteration):
        next(empty_rub_transactions)


@pytest.mark.usefixtures("transactions")
def test_filter_by_currency_no_amount(transactions):  # type: ignore[no-untyped-def]
    """
    Тест на случай списка транзакций без соответствующих валютных операций.
    """
    transactions_without_amount = [
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        }
    ]

    rub_transactions = filter_by_currency(transactions_without_amount, "RUB")

    # Проверяем, что генератор не выдает никаких значений и завершается без ошибок
    with pytest.raises(StopIteration):
        next(rub_transactions)


def test_transaction_descriptions_with_transactions(transactions):  # type: ignore[no-untyped-def]
    """
    Проверяем, что функция возвращает корректные описания для каждой транзакции.
    """
    descriptions = list(transaction_descriptions(transactions))
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert descriptions == expected_descriptions


def test_transaction_descriptions_with_empty_transactions():  # type: ignore[no-untyped-def]
    """
    Проверяем, что функция возвращает пустой список при пустом входном списке транзакций.
    """
    empty_transactions = []
    descriptions = list(transaction_descriptions(empty_transactions))
    assert descriptions == []


def test_transaction_descriptions_with_one_transaction(transactions):  # type: ignore[no-untyped-def]
    """
    Проверяем, что функция возвращает корректное описание для одной транзакции.
    """
    single_transaction = [transactions[0]]
    descriptions = list(transaction_descriptions(single_transaction))
    assert descriptions == ["Перевод организации"]


def test_transaction_descriptions_with_no_description(transactions):  # type: ignore[no-untyped-def]
    """
    Проверяем, что функция возвращает пустой список при отсутствии описания в транзакции.
    """
    transactions[0].pop("description", None)
    descriptions = list(transaction_descriptions(transactions))
    expected_descriptions = [
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert descriptions == expected_descriptions


@pytest.mark.parametrize("transactions_count", [2, 3, 4, 5])
def test_transaction_descriptions_with_various_count(transactions, transactions_count):  # type: ignore[no-untyped-def]
    """
    Проверяем, что функция возвращает корректные описания для различного количества транзакций.
    """
    selected_transactions = transactions[:transactions_count]
    descriptions = list(transaction_descriptions(selected_transactions))
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ][:transactions_count]
    assert descriptions == expected_descriptions


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 4, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003", "0000 0000 0000 0004"]),
        (1234, 1237, ["0000 0000 0000 1234", "0000 0000 0000 1235", "0000 0000 0000 1236", "0000 0000 0000 1237"]),
        (9995, 9998, ["0000 0000 0000 9995", "0000 0000 0000 9996", "0000 0000 0000 9997", "0000 0000 0000 9998"]),
        (123456789012345, 123456789012347, ["0123 4567 8901 2345", "0123 4567 8901 2346", "0123 4567 8901 2347"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator(start, end, expected):  # type: ignore[no-untyped-def]
    """
    Проверяем, что генератор выдает правильные номера карт в заданном диапазоне,
    корректность форматирования номеров карт, а так же что корректно обрабатывает
    крайние значения диапазона и правильно завершает генерацию.
    """
    generated_numbers = list(card_number_generator(start, end))
    assert generated_numbers == expected
