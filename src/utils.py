import json
import logging
import os

# Создаем директорию logs в корне проекта
logs_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(logs_dir, exist_ok=True)

# Путь к файлу лога
log_file_path = os.path.join(logs_dir, "utils.log")

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.handlers.clear()  # Удаляем старые handlers

# FileHandler
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Формат лога
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(module)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем handler
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list:
    """
    Загружает список транзакций из JSON-файла.

    :param file_path: Путь к JSON-файлу
    :return: Список словарей с данными о транзакциях или пустой список
    """
    logger.debug("Вызов функции load_transactions с аргументом: %s", file_path)

    if not isinstance(file_path, str):
        logger.error("file_path должен быть строкой.")
        raise TypeError("file_path должен быть строкой")
    try:
        if not os.path.exists(file_path):
            logger.warning("Файл %s не найден.", file_path)
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            logger.info("Успешно загружено %d транзакций из файла %s.", len(data), file_path)
            return data
        else:
            logger.warning("Файл %s содержит данные, не являющиеся списком.", file_path)
            return []
    except json.JSONDecodeError as e:
        logger.error("Ошибка при чтении JSON из файла %s: %s", file_path, e)
        return []
    except FileNotFoundError as e:
        logger.error("Файл %s не найден: %s", file_path, e)
        return []
    except Exception as e:
        logger.exception("Неизвестная ошибка при загрузке транзакций: %s", e)
        return []
