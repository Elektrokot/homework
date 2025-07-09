import unittest
from unittest.mock import MagicMock, patch

import requests

from src.external_api import convert_to_rub, get_currency_rate, get_exchange_rates


class TestExternalAPI(unittest.TestCase):

    # Тест для успешного получения курса
    @patch("src.external_api.requests.get")
    def test_get_currency_rate_success(self, mock_get): # type: ignore[no-untyped-def]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "quotes": {"USDRUB": 75.5}}
        mock_get.return_value = mock_response

        result = get_currency_rate("USD")
        self.assertAlmostEqual(result, 75.5, delta=0.01)

    # Тест для ошибки API (например, invalid base currency)
    @patch("src.external_api.requests.get")
    def test_get_currency_rate_api_error(self, mock_get): # type: ignore[no-untyped-def]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": False, "message": "invalid base currency"}
        mock_get.return_value = mock_response

        result = get_currency_rate("USD")
        self.assertEqual(result, 0.0)

    # Тест для сетевой ошибки (например, ConnectionError)
    @patch("src.external_api.requests.get")
    def test_get_currency_rate_connection_error(self, mock_get): # type: ignore[no-untyped-def]
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        result = get_currency_rate("USD")
        self.assertEqual(result, 0.0)

    # Тест для таймаута
    @patch("src.external_api.requests.get")
    def test_get_currency_rate_timeout_error(self, mock_get): # type: ignore[no-untyped-def]
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")

        result = get_currency_rate("USD")
        self.assertEqual(result, 0.0)

    # Тест для некорректного JSON
    @patch("src.external_api.requests.get")
    def test_get_currency_rate_invalid_json(self, mock_get): # type: ignore[no-untyped-def]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = get_currency_rate("USD")
        self.assertEqual(result, 0.0)

    # Тест для get_exchange_rates (успешный случай)
    @patch("src.external_api.get_currency_rate")
    def test_get_exchange_rates(self, mock_get_currency_rate): # type: ignore[no-untyped-def]
        mock_get_currency_rate.side_effect = [75.0, 85.0]  # USD, EUR

        result = get_exchange_rates()
        self.assertEqual(result, {"USD": 75.0, "EUR": 85.0})

    # Тест для get_exchange_rates, когда один из запросов неудачен
    @patch("src.external_api.get_currency_rate")
    def test_get_exchange_rates_with_failure(self, mock_get_currency_rate): # type: ignore[no-untyped-def]
        mock_get_currency_rate.side_effect = [75.0, 0.0]  # USD, EUR

        result = get_exchange_rates()
        self.assertEqual(result, {"USD": 75.0, "EUR": 0.0})

    # Тест для convert_to_rub (USD → RUB)
    def test_convert_usd_to_rub(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 75.0, "EUR": 85.0}
        result = convert_to_rub(100, "USD", exchange_rates)
        self.assertAlmostEqual(result, 7500.0, delta=0.01)

    # Тест для convert_to_rub (EUR → RUB)
    def test_convert_eur_to_rub(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 75.0, "EUR": 85.0}
        result = convert_to_rub(100, "EUR", exchange_rates)
        self.assertAlmostEqual(result, 8500.0, delta=0.01)

    # Тест для convert_to_rub (RUB → RUB)
    def test_convert_rub_to_rub(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 75.0, "EUR": 85.0}
        result = convert_to_rub(500, "RUB", exchange_rates)
        self.assertEqual(result, 500.0)

    # Тест для строки в convert_to_rub
    def test_convert_string_amount_to_rub(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 75.0}
        result = convert_to_rub("100", "USD", exchange_rates)
        self.assertAlmostEqual(result, 7500.0, delta=0.01)

    # Тест для отрицательной суммы
    def test_convert_negative_amount(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 75.0}
        result = convert_to_rub(-100, "USD", exchange_rates)
        self.assertAlmostEqual(result, -7500.0, delta=0.01)

    # Тест для некорректной строки (не число)
    def test_convert_invalid_string_amount_raises_value_error(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 75.0}
        with self.assertRaises(ValueError):
            convert_to_rub("invalid", "USD", exchange_rates)

    # Тест для None как amount
    def test_convert_none_amount_raises_type_error(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 75.0}
        with self.assertRaises(TypeError):
            convert_to_rub(None, "USD", exchange_rates)

    # Тест для нулевого курса
    def test_convert_with_zero_rate(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 0.0}
        result = convert_to_rub(100, "USD", exchange_rates)
        self.assertEqual(result, 0.0)

    # Тест для отсутствующей валюты в exchange_rates
    def test_convert_with_missing_currency(self): # type: ignore[no-untyped-def]
        exchange_rates = {"USD": 75.0}
        result = convert_to_rub(100, "EUR", exchange_rates)
        self.assertEqual(result, 0.0)
