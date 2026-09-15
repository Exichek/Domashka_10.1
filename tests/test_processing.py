import pytest

from src.processing import (filter_by_state, process_bank_operations,
                            process_bank_search, sort_by_date)


@pytest.fixture
def operations() -> list[dict]:
    """Возвращает тестовый список банковских операций."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2018-06-30T02:08:58.425572",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2020-01-15T12:00:00.000000",
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "2020-01-15T12:00:00.000000",
        },
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(
    operations: list[dict],
    state: str,
    expected_ids: list[int],
) -> None:
    result = filter_by_state(operations, state)

    assert [operation["id"] for operation in result] == expected_ids


def test_filter_by_state_default(operations: list[dict]) -> None:
    result = filter_by_state(operations)

    assert [operation["id"] for operation in result] == [1, 3]


def test_sort_by_date_descending(operations: list[dict]) -> None:
    result = sort_by_date(operations)

    assert [operation["id"] for operation in result] == [3, 4, 1, 2]


def test_sort_by_date_ascending(operations: list[dict]) -> None:
    result = sort_by_date(operations, reverse=False)

    assert [operation["id"] for operation in result] == [2, 1, 3, 4]


def test_sort_by_date_same_dates(operations: list[dict]) -> None:
    result = sort_by_date(operations)

    same_date_operations = [
        operation["id"]
        for operation in result
        if operation["date"] == "2020-01-15T12:00:00.000000"
    ]

    assert same_date_operations == [3, 4]


def test_process_bank_search() -> None:
    """Проверяет поиск транзакций по строке в описании."""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод со счета на счет"},
    ]

    result = process_bank_search(transactions, "Перевод")

    assert result == [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
    ]


def test_process_bank_search_ignore_case() -> None:
    """Проверяет поиск без учета регистра."""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]

    result = process_bank_search(transactions, "пЕрЕвОд")

    assert result == [
        {"description": "Перевод организации"},
    ]


def test_process_bank_search_no_matches() -> None:
    """Проверяет поиск при отсутствии совпадений."""
    transactions = [
        {"description": "Открытие вклада"},
    ]

    result = process_bank_search(transactions, "Перевод")

    assert result == []


def test_process_bank_operations() -> None:
    """Проверяет подсчет транзакций по категориям."""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
    ]

    categories = [
        "Перевод организации",
        "Открытие вклада",
        "Оплата",
    ]

    result = process_bank_operations(transactions, categories)

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Оплата": 0,
    }
