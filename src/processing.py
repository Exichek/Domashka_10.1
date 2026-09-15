import re
from collections import Counter
from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]],
    state: str = "EXECUTED",
) -> list[dict[str, Any]]:
    """Фильтрует список банковских операций по состоянию."""
    return [
        operation
        for operation in operations
        if operation.get("state") == state
    ]


def sort_by_date(
    operations: list[dict[str, Any]],
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Сортирует список банковских операций по ключу date."""
    return sorted(
        operations,
        key=lambda operation: operation["date"],
        reverse=reverse,
    )


def process_bank_search(
    data: list[dict[str, Any]],
    search: str,
) -> list[dict[str, Any]]:
    """Возвращает транзакции, содержащие строку поиска в описании."""
    pattern = re.escape(search)

    return [
        transaction
        for transaction in data
        if re.search(
            pattern,
            str(transaction.get("description", "")),
            re.IGNORECASE,
        )
    ]


def process_bank_operations(
    data: list[dict[str, Any]],
    categories: list[str],
) -> dict[str, int]:
    """Подсчитывает количество транзакций по заданным категориям."""
    descriptions = [
        str(transaction.get("description", ""))
        for transaction in data
    ]

    counter = Counter(descriptions)

    return {
        category: counter[category]
        for category in categories
    }
