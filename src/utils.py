import json
import os


def load_transactions(file_path: str) -> list:
    """
    Загружает список транзакций из JSON-файла.

    :param file_path: Путь к JSON-файлу
    :return: Список словарей с данными о транзакциях или пустой список
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path должен быть строкой")
    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []
