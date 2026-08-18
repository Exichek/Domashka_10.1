def filter_by_state(operations: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """Фильтрует список банковских операций по состоянию."""
    return [operation for operation in operations if operation["state"] == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список банковских операций по ключу date"""
    return sorted(operations, key=lambda operation: operation["date"], reverse=reverse)
