import pytest

from src.widget import get_date, mask_account_card


def test_get_date(date_test: str):  # type: ignore[no-untyped-def]
    assert get_date(date_test) == "11.03.2024"


@pytest.mark.parametrize(
    "string, expected_result",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
    ],
)
def test_mask_account_card(string: str, expected_result: str):  # type: ignore[no-untyped-def]
    assert mask_account_card(string) == expected_result
