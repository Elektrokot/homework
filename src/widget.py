from .masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """Функция обрабатывает информацию как о картах,
    так и о счетах и возвращает строку с замаскированным номером."""

    if "Счет" in card_info:
        return f"{card_info[:5]}{get_mask_account(card_info)}"
    else:
        return f"{card_info[:-16]}{get_mask_card_number(card_info[-16:])}"


def get_date(date_str: str) -> str:
    """Функция принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'."""

    return f"{date_str[8:10]}.{date_str[5:7]}.{date_str[:4]}"
