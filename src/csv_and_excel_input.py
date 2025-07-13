import csv
import os
from typing import Any, Dict, List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей.

    :param file_path: Путь к CSV-файлу.
    :return: Список транзакций в виде словарей или пустой список при ошибке.
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path должен быть строкой.")

    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            return [row for row in reader]

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

        df = pd.read_excel(file_path)
        # Преобразуем ключи в строки
        records = df.to_dict(orient="records")
        return [{str(k): v for k, v in record.items()} for record in records]

    except (FileNotFoundError, pd.errors.ParserError, UnicodeDecodeError) as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
        return []
