import re
from collections import Counter
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Функция фильтрует список словарей с данными о банковских операциях,
    оставляя только те, у которых в описании есть заданная строка (регистронезависимо).

    :param data: Список словарей с данными о банковских операциях.
    :param search: Строка для поиска в описании операции.
    :return: Отфильтрованный список словарей.
    """
    if not isinstance(data, list):
        raise TypeError("data должен быть списком.")
    if not isinstance(search, str):
        raise TypeError("search должен быть строкой.")

    # Компилируем регулярное выражение для регистронезависимого поиска
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    # Фильтруем данные, проверяя наличие совпадений в описании
    filtered_data = [item for item in data if "description" in item and pattern.search(item["description"])]

    return filtered_data


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Функция подсчитывает количество операций для каждой категории.

    :param data: Список словарей с данными о банковских операциях.
    :param categories: Список категорий операций.
    :return: Словарь, где ключи — это названия категорий, а значения — количество операций.
    """
    if not isinstance(data, list):
        raise TypeError("data должен быть списком.")
    if not isinstance(categories, list):
        raise TypeError("categories должен быть списком.")

    # Создаем счетчик для категорий
    category_counts = Counter({category: 0 for category in categories})  # type: ignore

    # Подсчитываем операции для каждой категории
    for operation in data:
        description = operation.get("description", "").lower()  # Преобразуем описание в нижний регистр
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1

    # Возвращаем результат как обычный словарь
    return dict(category_counts)
