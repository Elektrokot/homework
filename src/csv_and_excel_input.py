import csv
import os
from typing import Any, Dict, List

import pandas as pd


def read_csv_transactions(
    file_path: str,
) -> list[dict[str, dict[str, dict[str, str | Any] | str | Any] | str | Any | None]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей.
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path должен быть строкой.")

    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            transactions = []
            for row in reader:
                # Преобразуем данные в структуру, аналогичную JSON
                transaction = {
                    "id": row.get("id"),
                    "state": row.get("state"),
                    "date": row.get("date"),
                    "description": row.get("description"),
                    "from": row.get("from"),
                    "to": row.get("to"),
                    "operationAmount": {
                        "amount": row.get("amount", "0"),
                        "currency": {
                            "name": row.get("currency_name", "руб."),
                            "code": row.get("currency_code", "RUB"),
                        },
                    },
                }
                transactions.append(transaction)

            return transactions

    except (FileNotFoundError, csv.Error, UnicodeDecodeError) as e:
        print(f"Ошибка при чтении CSV-файла: {e}")
        return []


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла и возвращает список словарей.

    :param file_path: Путь к Excel-файлу.
    :return: Список транзакций в виде словарей или пустой список при ошибке.
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path должен быть строкой.")

    try:
        if not os.path.exists(file_path):
            return []

        # Чтение данных из Excel
        df = pd.read_excel(file_path, dtype=str)

        # Преобразование DataFrame в список словарей
        transactions = []
        for _, row in df.iterrows():
            transaction = {
                "id": row.get("id"),
                "state": row.get("state"),
                "date": row.get("date"),
                "description": row.get("description"),
                "from": row.get("from"),
                "to": row.get("to"),
                "operationAmount": {
                    "amount": row.get("amount", "0"),
                    "currency": {
                        "name": row.get("currency_name", "руб."),
                        "code": row.get("currency_code", "RUB"),
                    },
                },
            }
            transactions.append(transaction)

        return transactions

    except (FileNotFoundError, pd.errors.ParserError, UnicodeDecodeError) as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
        return []
