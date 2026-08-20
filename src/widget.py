from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_or_card_number: str) -> str:
    """Маскирует номер банковской карты или счета."""
    parts = account_or_card_number.split()

    if len(parts) < 2:
        raise ValueError("Введите тип карты или счета и его номер")

    name = " ".join(parts[:-1])
    number = parts[-1]

    if not number.isdigit():
        raise ValueError("Номер должен состоять только из цифр")

    if name == "Счет":
        return f"{name} {get_mask_account(number)}"

    return f"{name} {get_mask_card_number(number)}"


def get_date(date: str) -> str:
    """Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ."""
    date_parts = datetime.fromisoformat(date)

    return date_parts.strftime("%d.%m.%Y")
