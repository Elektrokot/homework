def get_mask_card_number(card_number):
    """Функция преобразования введенного числа в номер карты с маскировкой 6 цифр."""

    # Проверяем, что вход это строка или число, которое можно преобразовать в строку
    if not isinstance(card_number, (int, str)):
        raise ValueError("Номер карты должен быть числом или строкой.")

    # Преобразуем число в строку для удобства работы со строками
    card_number_str = str(card_number)

    # Убираем все неподходящие символы (например, пробелы и тире)
    cleaned_card_number_str = ''.join(char for char in card_number_str if char.isdigit())

    # Проверяем, что длина номера карты находится в допустимом диапазоне (от 13 до 19 цифр)
    # согласно информации из поисковика Google.
    if not (13 <= len(cleaned_card_number_str) <= 19):
        raise ValueError("Номер карты должен содержать от 13 до 19 цифр.")

    # Формируем маску в зависимости от длины номера карты
    if len(cleaned_card_number_str) == 13:
        masked_card_number = (f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}"
                              f"** **** {cleaned_card_number_str[-1:]}")

    elif len(cleaned_card_number_str) == 15:
        masked_card_number = (f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}"
                              f"** **** {cleaned_card_number_str[-3:]}")

    elif len(cleaned_card_number_str) == 16:
        masked_card_number = (f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}"
                              f"** **** {cleaned_card_number_str[-4:]}")

    elif len(cleaned_card_number_str) == 18:
        masked_card_number = (f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}"
                              f"** **** {cleaned_card_number_str[-2:]}")

    elif len(cleaned_card_number_str) == 19:
        masked_card_number = (f"{cleaned_card_number_str[:4]} {cleaned_card_number_str[4:6]}"
                              f"** **** {cleaned_card_number_str[-3:]}")

    return masked_card_number

def get_mask_account(account_number):
    """Функция принимает на вход номер счёта и выдает его обратно с маской в виде **ХХХХ."""

    # Проверяем, что вход это строка или число, которое можно преобразовать в строку
    if not isinstance(account_number, (int, str)):
        raise ValueError("Номер счета должен быть числом или строкой.")

    # Преобразуем число в строку для удобства работы со строками
    account_number_str = str(account_number)

    # Убираем текст и оставляем только цифры счёта
    cleaned_account_number_str = ''.join(char for char in account_number_str if char.isdigit())

    # Проверяем, что длина номера счета соответствует стандартным требованиям (обычно 20 цифр)
    if len(cleaned_account_number_str) != 20:
        raise ValueError("Номер счета должен содержать ровно 20 цифр.")

    # Формируем маску
    masked_account_number = f"**{cleaned_account_number_str[-4:]}"

    return masked_account_number
