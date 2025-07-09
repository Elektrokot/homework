from typing import Dict, Iterator, List


def filter_by_currency(transactions: List[Dict], currency_code: str) -> Iterator[Dict]:
    """
    Функция возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD).
    """
    for transaction in transactions:
        if "operationAmount" in transaction and "currency" in transaction["operationAmount"]:
            if transaction["operationAmount"]["currency"]["code"] == currency_code:
                yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди.
    """
    for transaction in transactions:
        if "description" in transaction:
            yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX.
    Генератор может сгенерировать номера карт в заданном диапазоне
    от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    """
    for number in range(start, stop + 1):
        formatted_number = f"{number:016d}"
        yield f"{formatted_number[0:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:16]}"
