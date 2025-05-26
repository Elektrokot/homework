from typing import Dict, List


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """ Функция фильтрует список транзакций по состоянию. """

    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """ Функция сортирует список транзакций по дате. """

    return sorted(transactions, key=lambda x: x.get("date", ""), reverse=reverse)
