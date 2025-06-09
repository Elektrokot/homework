import pytest
from typing import Dict, List


from src.processing import filter_by_state, sort_by_date
from tests.conftest import transactions


def test_filter_by_state(transactions):
    # Фильтруем транзакции по состоянию 'EXECUTED'
    executed_transactions = filter_by_state(transactions, "EXECUTED")

    # Ожидаемые транзакции с состоянием 'EXECUTED'
    expected_executed_transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
    ]

    # Проверяем, что фильтрованные транзакции соответствуют ожидаемым
    assert executed_transactions == expected_executed_transactions

    # Фильтруем транзакции по состоянию 'CANCELED'
    canceled_transactions = filter_by_state(transactions, "CANCELED")

    # Ожидаемые транзакции с состоянием 'CANCELED'
    expected_canceled_transactions = [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
    ]

    # Проверяем, что фильтрованные транзакции соответствуют ожидаемым
    assert canceled_transactions == expected_canceled_transactions


def test_sort_by_date(transactions: List[Dict]):
    # Сортируем транзакции по дате в порядке убывания
    sorted_transactions_desc = sort_by_date(transactions, reverse=True)

    # Ожидаемые транзакции в порядке убывания даты
    expected_sorted_transactions_desc = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
    ]

    # Проверяем, что отсортированные транзакции соответствуют ожидаемым
    assert sorted_transactions_desc == expected_sorted_transactions_desc

    # Сортируем транзакции по дате в порядке возрастания
    sorted_transactions_asc = sort_by_date(transactions, reverse=False)

    # Ожидаемые транзакции в порядке возрастания даты
    expected_sorted_transactions_asc = [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}
    ]

    # Проверяем, что отсортированные транзакции соответствуют ожидаемым
    assert sorted_transactions_asc == expected_sorted_transactions_asc