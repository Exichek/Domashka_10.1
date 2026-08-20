import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account_or_card_number, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361",),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361",),
        ("Счет 73654108430135874305", "Счет **4305",),
    ],
)
def test_mask_account_card(account_or_card_number: str, expected: str) -> None:
    assert mask_account_card(account_or_card_number) == expected


@pytest.mark.parametrize(
    "incorrect_data",
    ["", "Visa", "Счет",],
)
def test_mask_account_card_without_number(incorrect_data: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(incorrect_data)


@pytest.mark.parametrize(
    "incorrect_data",
    [
        "Visa Platinum abcdef",
        "Счет 1234abcd",
    ],
)
def test_mask_account_card_invalid_number(incorrect_data: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(incorrect_data)


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-08-26T10:50:58.294041", "26.08.2019"),
        ("2020-01-01T00:00:00", "01.01.2020"),
    ],
)
def test_get_date(date: str, expected: str) -> None:
    assert get_date(date) == expected


@pytest.mark.parametrize(
    "incorrect_date",
    ["", "не дата", "2024-99-99",],
)
def test_get_date_invalid(incorrect_date: str) -> None:
    with pytest.raises(ValueError):
        get_date(incorrect_date)
