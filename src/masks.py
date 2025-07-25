import logging
import os

# Создаем директорию logs в корне проекта
logs_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(logs_dir, exist_ok=True)

# Путь к файлу лога
log_file_path = os.path.join(logs_dir, "masks.log")

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


def get_mask_card_number(card_number: str) -> str:
    """Функция преобразования введенного числа в номер карты с маскировкой 6 цифр."""

    logger.debug("Вызов функции get_mask_card_number с аргументом: %s", card_number)

    # Проверка на пустые значения
    if not card_number or not isinstance(card_number, str):
        raise ValueError("Номер карты не может быть пустым.")

    # Проверяем, что вход это строка или число, которое можно преобразовать в строку
    if not isinstance(card_number, str):
        logger.error("Номер карты должен быть строкой.")
        raise ValueError("Номер карты должен быть строкой.")

    # Преобразуем число в строку для удобства работы со строками
    card_number_str = str(card_number)

    # Убираем все неподходящие символы (например, пробелы и тире)
    cleaned_card_number_str = "".join(char for char in card_number_str if char.isdigit())

    # Проверяем, что длина номера карты находится в допустимом диапазоне (от 13 до 19 цифр)
    # согласно информации из поисковика Google.
    if not (13 <= len(cleaned_card_number_str) <= 19):
        logger.error("Номер карты должен содержать от 13 до 19 цифр.")
        raise ValueError("Номер карты должен содержать от 13 до 19 цифр.")

    # Формируем маску в зависимости от длины номера карты
    if len(cleaned_card_number_str) == 13:
        masked_card_number = (
            f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}" f"** **** {cleaned_card_number_str[-1:]}"
        )

    elif len(cleaned_card_number_str) == 15:
        masked_card_number = (
            f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}" f"** **** {cleaned_card_number_str[-3:]}"
        )

    elif len(cleaned_card_number_str) == 16:
        masked_card_number = (
            f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}" f"** **** {cleaned_card_number_str[-4:]}"
        )

    elif len(cleaned_card_number_str) == 18:
        masked_card_number = (
            f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}" f"** **** {cleaned_card_number_str[-2:]}"
        )

    elif len(cleaned_card_number_str) == 19:
        masked_card_number = (
            f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}" f"** **** {cleaned_card_number_str[-3:]}"
        )
    logger.info("Маскированный номер карты: %s", masked_card_number)
    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счёта и выдает его обратно с маской в виде **ХХХХ."""

    logger.debug("Вызов функции get_mask_account с аргументом: %s", account_number)

    # Проверяем, что вход это строка или число, которое можно преобразовать в строку
    if not isinstance(account_number, str):
        logger.error("Номер счета должен быть строкой.")
        raise ValueError("Номер счета должен быть строкой.")

    # Преобразуем число в строку для удобства работы со строками
    account_number_str = str(account_number)

    # Убираем текст и оставляем только цифры счёта
    cleaned_account_number_str = "".join(char for char in account_number_str if char.isdigit())

    # Проверяем, что длина номера счета соответствует стандартным требованиям (обычно 20 цифр)
    if len(cleaned_account_number_str) != 20:
        logger.error("Номер счета должен содержать ровно 20 цифр.")
        raise ValueError("Номер счета должен содержать ровно 20 цифр.")

    # Формируем маску
    masked_account_number = f"**{cleaned_account_number_str[-4:]}"
    logger.info("Маскированный номер счета: %s", masked_account_number)
    return masked_account_number
