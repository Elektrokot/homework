import os
from typing import Union, cast

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_currency_rate(base_currency: str) -> float:
    """
    Получает курс указанной валюты к RUB.

    :param base_currency: Базовая валюта (например, USD или EUR)
    :return: Курс (float) или 0.0 при ошибке
    """
    url = f"https://api.apilayer.com/currency_data/live?source={base_currency}&currencies=RUB"
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            value = data["quotes"].get(f"{base_currency}RUB", 0.0)
            return cast(float, value)
        else:
            print(f"Ошибка при получении курса {base_currency}:", data.get("message"))
            return 0.0
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Ошибка сети или формата данных для {base_currency}:", e)
        return 0.0


def get_exchange_rates() -> dict:
    """
    Получает курсы USD и EUR к RUB в двух отдельных запросах.

    :return: Словарь с курсами {'USD': rate, 'EUR': rate}
    """
    return {"USD": get_currency_rate("USD"), "EUR": get_currency_rate("EUR")}


def convert_to_rub(amount: Union[str, float], currency: str, exchange_rates: dict[str, float]) -> float:
    """
    Конвертирует сумму в RUB на основе переданных курсов.

    :param amount: Сумма транзакции
    :param currency: Код валюты (например, USD, EUR, RUB)
    :param exchange_rates: Словарь с курсами {'USD': rate, 'EUR': rate}
    :return: Сумма в рублях (float)
    """
    if currency == "RUB":
        return float(amount)

    rate = exchange_rates.get(currency, 0.0)
    if rate <= 0:
        print(f"Некорректный курс для {currency}: {rate}")
        return float(0.0)

    return float(amount) * rate
