def get_mask_card_number(card_number: str) -> str:
    """Функция преобразования введенного числа в номер карты с маскировкой 6 цифр."""

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счёта и выдает его обратно с маской в виде **ХХХХ."""

    return f"**{account_number[-4:]}"
