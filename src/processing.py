def filter_by_state(operations: list[dict], state: str ='EXECUTED') -> list[dict]:
    """Фильтрует список банковских операций по состоянию."""
    return [operation for operation in operations if operation["state"] == state]