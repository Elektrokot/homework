import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "string_card, expected_result_card",
    [
        ("1234567890123", "1234 56** **** 3"),
        ("1234567890123455", "1234 56** **** 3455"),
        ("123456789012345", "1234 56** **** 345"),
        ("1234-5678-9012-3459", "1234 56** **** 3459"),
        ("123456789012345678", "1234 56** **** 78"),
        ("1234-5678 - 9012 - 3456", "1234 56** **** 3456"),
        ("1234567890123456789", "1234 56** **** 789"),
        ("1234 5678 9012 3458", "1234 56** **** 3458"),
        ("1234-5678 - 9012 - 3457", "1234 56** **** 3457"),
    ],
)
def test_get_mask_card_number(string_card: str, expected_result_card: str):  # type: ignore[no-untyped-def]
    assert get_mask_card_number(string_card) == expected_result_card


@pytest.mark.parametrize("wrong_data_card", [123456789012, "12345678901234567890", None, ""])
def test_get_mask_card_number_wrong(wrong_data_card):  # type: ignore[no-untyped-def]
    with pytest.raises(ValueError):
        get_mask_card_number(wrong_data_card)


@pytest.mark.parametrize(
    "string_account, expected_result_account", [("35383033474447895560", "**5560"), ("73654108430135874305", "**4305")]
)
def test_get_mask_account(string_account: str, expected_result_account: str):  # type: ignore[no-untyped-def]
    assert get_mask_account(string_account) == expected_result_account


@pytest.mark.parametrize("wrong_data_account", [7365410843013587, "", None])
def test_get_mask_account_wrong(wrong_data_account):  # type: ignore[no-untyped-def]
    with pytest.raises(ValueError):
        get_mask_account(wrong_data_account)
